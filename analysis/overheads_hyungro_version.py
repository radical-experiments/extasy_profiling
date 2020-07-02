import matplotlib.pyplot as plt

#%run 'bin/notebook_utils.py'
#%run 'bin/plot_utilization.py'
import matplotlib.ticker as mticker
import radical.entk as re
import radical.analytics as ra
import radical.utils as ru
import radical.pilot as rp

# These are the "Tableau 20" colors as RGB.    
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)] 

import sys
if len(sys.argv) > 1:
    suds = sys.argv[1:]
else:
    suds = [ 're.session.login5.hrlee.018425.0013',
    #ttx_u is zero, eliminating for the moment, 're.session.login5.hrlee.018425.0017',
    're.session.login5.hrlee.018425.0018',
    're.session.login5.hrlee.018425.0020',
    're.session.login5.hrlee.018425.0021']

sids = [s for s in suds]

ss = {}
for sid in suds:
    sp = sid
    ss[sid] = {'s': ra.Session(sp, 'radical.pilot')}
    ss[sid].update({'p': ss[sid]['s'].filter(etype='pilot'   , inplace=False),
                    'u': ss[sid]['s'].filter(etype='unit'    , inplace=False),
                    't': ss[sid]['s'].filter(etype='task'    , inplace=False),
                    'w': ss[sid]['s'].filter(etype='pipeline', inplace=False)})

for sid in suds:

    ss[sid].update({'sid'   : ss[sid]['s'].uid,
                    'pid'   : ss[sid]['p'].list('uid'),
                    'npilot': len(ss[sid]['p'].get()),
                    'lm'    : ss[sid]['s'].get(etype='pilot')[0].cfg['agent_launch_method'],
                    'npact' : len(ss[sid]['p'].timestamps(state='PMGR_ACTIVE')),
                    'nunit' : len(ss[sid]['u'].get()),
                    'nudone': len(ss[sid]['u'].timestamps(state='DONE')),
                    'nufail': len(ss[sid]['u'].timestamps(state='FAILED'))})
    ss[sid].update({'pres'  : ss[sid]['p'].get(uid=ss[sid]['pid'])[0].description['resource'],
                    'ncores': ss[sid]['p'].get(uid=ss[sid]['pid'])[0].description['cores'],
                    'ngpus' : ss[sid]['p'].get(uid=ss[sid]['pid'])[0].description['gpus']})                  
    ss[sid].update({'nnodes': ss[sid]['ngpus']/6})

for sid in suds:
    print("""
%s:
\tName of the HPC platform: %s
\tPilot launch method: %s
\tNumber of pilots requested: %i
\tNumber of pilots active: %i
\tNumber of requested cores: %i
\tNumber of requested GPUs: %s
\tNumber of requested nodes: %s
\tNumber of nodes asked by ENTK: %i
\tNumber of tasks executed by EnTK: %i
\tNumber of tasks successfully executed by EnTK: %i
\tNumber of failed tasks: %i
""" % (sid              , ss[sid]['pres']  , ss[sid]['lm'], 
       ss[sid]['npilot'], ss[sid]['npact'] , ss[sid]['ncores']/4, 
       ss[sid]['ngpus'] , ss[sid]['nnodes'], ss[sid]['ncores']/168, 
       ss[sid]['nunit'] , ss[sid]['nudone'], ss[sid]['nufail']))

for sid in suds:
    w  = ss[sid]['w']
    u  = ss[sid]['u']
    t  = ss[sid]['t']
    p  = ss[sid]['p']
    p0 = p.get(uid=ss[sid]['pid'])[0]

    ss[sid].update({
      #'ttc'  : p0.duration(event=[ {ru.EVENT: 'state'        , ru.STATE: rp.NEW                }, 
      #                             {ru.EVENT: 'state'        , ru.STATE: rp.CANCELED           } ]),
      'ttq_p': p0.duration(event=[ {ru.EVENT: 'state'        , ru.STATE: rp.PMGR_ACTIVE_PENDING}, 
                                   {ru.EVENT: 'state'        , ru.STATE: rp.PMGR_ACTIVE        } ]),
      'ttx_w': w.duration( event=[ {ru.EVENT: 'state'        , ru.STATE: re.states.SCHEDULING  },
                                   [{ru.EVENT: 'state'        , ru.STATE: re.states.DONE        },
                                   {ru.EVENT: 'state'        , ru.STATE:
                                       re.states.COMPLETED             },
                                   {ru.EVENT: 'state'        , ru.STATE:
                                       re.states.FAILED             },
                                   {ru.EVENT: 'state'        , ru.STATE:
                                       re.states.CANCELED           }]]),
      'ttx_u': u.duration( event=[ {ru.EVENT: 'cu_exec_start', ru.STATE: None                  },      
                                   {ru.EVENT: 'cu_exec_stop' , ru.STATE: None                  } ]),
      'ttx_p': p0.duration(event=[ {ru.EVENT: 'state'        , ru.STATE: rp.PMGR_ACTIVE        },
                                  [{ru.EVENT: 'state'        , ru.STATE: rp.DONE               },
                                   {ru.EVENT: 'state'        , ru.STATE: rp.FAILED             },
                                   {ru.EVENT: 'state'        , ru.STATE: rp.CANCELED           }]]),
      'sub_t': t.duration( event=[ {ru.EVENT: 'state'        , ru.STATE: re.states.SCHEDULING  },
                                   {ru.EVENT: 'state'        , ru.STATE: re.states.SUBMITTING  } ]),
      'ttx_t': t.duration( event=[ {ru.EVENT: 'state'        , ru.STATE: re.states.SUBMITTING  },
                                  [{ru.EVENT: 'state'        , ru.STATE: re.states.COMPLETED   },
                                   {ru.EVENT: 'state'        , ru.STATE: re.states.CANCELED    },
                                   {ru.EVENT: 'state'        , ru.STATE: re.states.FAILED      }]])})

    # overall overhead 
    ss[sid].update({'ovh_rtc': ss[sid]['ttx_p'] - ss[sid]['ttx_u']})
    # starting up cost
    ss[sid].update({'ovh_startup':
        u.timestamps(event='cu_exec_start',state='AGENT_EXECUTING')[0] -
        p0.timestamps(state='PMGR_ACTIVE')[0]})
    # shutting down cost
    ss[sid].update({'ovh_shutdown':p0.timestamps(state='CANCELED')[0] -
        u.timestamps(state='AGENT_STAGING_OUTPUT_PENDING')[-1]})
    # entk cost
    ss[sid].update({'ovh_entk':ss[sid]['ttx_w'] - ss[sid]['ttx_u']})
    # RP cost
    ss[sid].update({'ovh_rp':
        ss[sid]['ttx_p'] - ss[sid]['ttx_w']})
    print ("{}:{},{},{},{},{}".format(sid, ss[sid]['ovh_rtc'],
    ss[sid]['ovh_startup'], ss[sid]['ovh_shutdown'], ss[sid]['ovh_entk'],
    ss[sid]['ovh_rp']))


fwidth = 18
fhight = 4
fig, axarr = plt.subplots(1, len(suds), sharey=True, figsize=(fwidth, fhight))

def autolabel(rects):

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height, '%d' %
                int(height), ha='center', va='bottom')

i = 0
j = 'a'
for sid in suds:
    
    ax = axarr[i] if len(suds) > 1 else axarr
    ax.title.set_text('%s/%s Tasks/Nodes' % (ss[sid]['nunit'], int(ss[sid]['nnodes'])))

    rects1 = ax.bar(x = 'OVH', height = ss[sid]['ovh_rtc'], color = 'r')
    rects2 = ax.bar(x = 'TTX', height = ss[sid]['ttx_u']  , color = 'b')
    
    ax.set_xlabel('(%s)' % j, labelpad=45)
    
    i = i+1
    j = chr(ord(j) + 1)
    autolabel(rects1)
    autolabel(rects2)


fig.text(0   ,  0.5 , 'Time (s)', va='center', rotation='vertical', fontsize=24)
fig.text(0.5 , -0.05, 'Metric'  , ha='center', fontsize=24)
fig.legend(['RADICAL Cybertools overhead (OVH)', 'Wokflow time to completion (TTX)'], loc='upper center', 
           bbox_to_anchor=(0.52, 1.6), fontsize=26, ncol=1)

plt.savefig('extasy_gromacs_overheads.pdf', dpi=300, bbox_inches='tight')
plt.savefig('extasy_gromacs_overheads.png', dpi=300, bbox_inches='tight')

### Additional plots
fig, axarr = plt.subplots(1, len(suds), sharey=True, figsize=(fwidth, fhight))

i = 0
j = 'a'
for sid in suds:
    
    ax = axarr[i] if len(suds) > 1 else axarr
    ax.title.set_text('%s/%s Tasks/Nodes' % (ss[sid]['nunit'], int(ss[sid]['nnodes'])))

    rects1 = ax.bar(x = 'OVH', height = ss[sid]['ovh_startup'], color = 'r')
    rects2 = ax.bar(x = 'TTX', height = ss[sid]['ttx_u']  , color = 'b')
    
    ax.set_xlabel('(%s)' % j, labelpad=45)
    
    i = i+1
    j = chr(ord(j) + 1)
    autolabel(rects1)
    autolabel(rects2)


fig.text(0   ,  0.5 , 'Time (s)', va='center', rotation='vertical', fontsize=24)
fig.text(0.5 , -0.05, 'Metric'  , ha='center', fontsize=24)
fig.legend(['RADICAL Cybertools overhead (OVH)', 'Wokflow time to completion (TTX)'], loc='upper center', 
           bbox_to_anchor=(0.52, 1.6), fontsize=26, ncol=1)

plt.savefig('extasy_gromacs_overheads_startup.pdf', dpi=300, bbox_inches='tight')
plt.savefig('extasy_gromacs_overheads_startup.png', dpi=300, bbox_inches='tight')


fig, axarr = plt.subplots(1, len(suds), sharey=True, figsize=(fwidth, fhight))

i = 0
j = 'a'
for sid in suds:
    
    ax = axarr[i] if len(suds) > 1 else axarr
    ax.title.set_text('%s/%s Tasks/Nodes' % (ss[sid]['nunit'], int(ss[sid]['nnodes'])))

    rects1 = ax.bar(x = 'OVH-START', height = ss[sid]['ovh_startup'], color = 'r')
    rects2 = ax.bar(x = 'OVH-END', height = ss[sid]['ovh_shutdown'], color = 'g')
    rects3 = ax.bar(x = 'OVH-ENTK', height = ss[sid]['ovh_entk'], color = 'm')
    rects4 = ax.bar(x = 'OVH-RP', height = ss[sid]['ovh_rp'], color = 'y')
    rects5 = ax.bar(x = 'TTX', height = ss[sid]['ttx_u']  , color = 'b')
    
    ax.set_xlabel('(%s)' % j, labelpad=45)
    
    i = i+1
    j = chr(ord(j) + 1)
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    autolabel(rects4)
    autolabel(rects5)


fig.text(0   ,  0.5 , 'Time (s)', va='center', rotation='vertical', fontsize=24)
fig.text(0.5 , -0.05, 'Metric'  , ha='center', fontsize=24)
fig.legend(['RADICAL Cybertools overhead (OVH)', 'Wokflow time to completion (TTX)'], loc='upper center', 
           bbox_to_anchor=(0.52, 1.6), fontsize=26, ncol=1)

plt.savefig('extasy_gromacs_overheads_breakdown.pdf', dpi=300, bbox_inches='tight')
plt.savefig('extasy_gromacs_overheads_breakdown.png', dpi=300, bbox_inches='tight')
