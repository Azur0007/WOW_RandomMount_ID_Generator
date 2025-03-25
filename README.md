# WOW_RandomMount_ID_Generator
Uses SimpleArmory and Wowhead to give you a list of mounts you don't own

______________________________________________________________________
***The scripts use the following libraries***
	
	SimpleArmoryGather
		selenium
		webdriver_manager
		re
		time
		json

	cache builder Mounts
		requests
		re
		json
		os
	
	MountAPI
		tkinter
		random
		json
		os
		webbrowser
		PIL
		io
		requests
______________________________________________________________________

To use the script, follow the steps below:

1) Open SimpleArmoryGather and insert your character's info (Region, Realm, Name) and run it. Move to step 2 when the console says "Saved IDs in missingMounts.json"

2) Open CacheBuilderMounts and run it without changing anything. This might take a while since it's gathering every missing mount from wowhead. Move to step 3 once the console says "Done. Saved {Number} items to {Path}"

3) Open MountAPI and run it. This is the script that you will be using to generate mount IDs. Insert a number, click generate.
______________________________________________________________________

***Extra info***
	- "Remove" deletes the item from the Structured_Cache list permanently, so only click it once a mount has been collected. If you delete an item by accident, run the CacheBuilderMounts script again.
	- I have not tested this script thoroughly enough to guarantee that it will work everyone.
	- I added tons of comments in the scripts for readability.
	- It's my first GitHub post, so this whole thing is probably gonna look different than what you are used to.
	- The scripts should automatically make all the relevant JSON files for you.
______________________________________________________________________
