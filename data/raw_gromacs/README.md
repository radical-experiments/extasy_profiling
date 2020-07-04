### Description

(Ascending order of Task Count, and Session ID)

| Session ID                                 | Task Count | Resource| iters | Note |
| ------------------------------------------ | ---------- | ------- | ----- | ---- |
| re.session.login5.hrlee.018446.0000.tar.gz | 120        | 120 gpus| 1     | **hotfix/prte_profiling** |
| re.session.login3.hrlee.018445.0002.tar.gz | 240        | 240 gpus| 1     | **hotfix/prte_profiling** |
| re.session.login3.hrlee.018445.0004.tar.gz | 480        | 480 gpus| 1     | **hotfix/prte_profiling** |
| re.session.login3.hrlee.018445.0001.tar.gz | 960        | 960gpus | 1     | **hotfix/prte_profiling** |
| ~~re.session.login5.hrlee.018445.0005.tar.gz~~ | 1920       | 1920gpus| 1     | Broken, **hotfix/prte_profiling** |
| re.session.login1.hrlee.018446.0004.tar.gz | 1920       | 1920gpus| 1     | **hotfix/prte_profiling** |
| re.session.login1.hrlee.018446.0005.tar.gz | 3840       | 3849gpus| 1     | FAILED 411/3840 |


### Outdated

| Session ID                                 | Task Count | Resource| iters | Note |
| ------------------------------------------ | ---------- | ------- | ----- | ---- |
| re.session.login5.hrlee.018425.0013.tar.gz | 60         | 60 gpus | 1     |      |
| re.session.login5.hrlee.018425.0017.tar.gz | 120        | 120 gpus| 1     |      |
| re.session.login5.hrlee.018425.0018.tar.gz | 240        | 240 gpus| 1     |      |
| re.session.login3.hrlee.018443.0007.tar.gz | 240        | 240 gpus| 1     | NEW|
| ~~re.session.login5.hrlee.018425.0020.tar.gz~~ | 480        | 480 gpus| 1     | broken |
| re.session.login5.hrlee.018425.0020-fixed.tar.bz | 480    | 480 gpus| 1    | fixed  |
| ~~re.session.login1.hrlee.018429.0030.tar.gz~~ | 1920     | 1920gpus| 1     | broken |
| re.session.login4.hrlee.018431.0000.tar.gz | 1920       | 1920gpus| 1     |      |
| re.session.login1.hrlee.018443.0011.tar.gz | 1920       | 1920gpus| 1     |NEW|

**re.session.login3.hrlee.018443.0007.tar.gz** includes new PR, reduced RMQ synchronization at EnTK, i.e. https://github.com/radical-cybertools/radical.entk/pull/466. 
**re.session.login1.hrlee.018443.0011.tar.gz** includes new PR, reduced RMQ synchronization at EnTK, i.e. https://github.com/radical-cybertools/radical.entk/pull/466. 

## N iteration

| Session ID                                 | Task Count | Resource| iters |
| ------------------------------------------ | ---------- | ------- | ----- |
| re.session.login5.hrlee.018425.0021.tar.gz | 960        | 960 gpus| 1     |
| re.session.login4.hrlee.018430.0000.tar.gz | 960        | 480 gpus| 2     |
| re.session.login5.hrlee.018430.0004.tar.gz | 960        | 240 gpus | 4    |


