I must name all my experiments by date - much easier to work this way. 

prompts are in tasks/

for each tasks/prompt1.md there is tasks/prompt1_out.md -> which notifies of changes that were done. 

for each tasks/prompt1.md -> there is 
- src/prompt1_ suffix to any code files created 
- logs/prompt1_ suffix to any logs created 
- data/prompt1_ suffix to any data that needs to be created
- out/prompt1_ suffix to any results (output). could be in the form of a folder 

if new version of a file is created - do _v1, _v2, etc 
if new version of a file is created on different date -> copy to new folder (date) -> and name there as prompt1_..._v2.py accordingly

src/ - has the master copy of everything... that is currently working 

there is also 'brainstorm' folder with early goals 
0. init_prompt 
1. brainstorm 
- brainstorm_user_needs
- brainstorm_tools
- brainstorm_tests 

in the tasks folder, there is 'overview' folder where concrete steps on macro scale are given (and edited accordingly )-
- prd.md 
- plan_phase1.md -> first phase 




----------------------------


--wip--
        --- s20251206_task1/
                    src 
                        ---task1_v1.*py|sh
                    input
                    output
                        ---task1_v1_out/
                        ---task1_v2_out/
                    logs
                        ---task1_v1_logs/
                        ---task1_v2_logs/

---01 brainstorm 
---02 plan
---03 tasks
    ---task1.md 
    ---task1_out.md 

---src
---input
---output
---logs

