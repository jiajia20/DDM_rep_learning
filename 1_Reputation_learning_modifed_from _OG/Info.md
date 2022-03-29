## Info

This is the first attempt to include reputation learning in the original binary choice game. 

In this version I used alhazen to run many different game in parallel.

This version the reputation information **are NOT** record properly because the parallel processing. The reputation information are wiped each round while it is actually suppose to be kept for future learning purpose. 

There are three verision:
**study_with_alter** is the orginia version that use a gobal variable to record the reputation information.

**study_annotated** is the version with 12 agents (the fully-conetced condition is buggy too.

**study_small** is the the version with 6 agents
