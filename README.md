## ProxyEdge/Glass Lewis 

Code does the following:

1. downloads the meeting lists for all the IDs (or IDs we specify) and saves them down in a specified path
2. creates folders based on company names from the ID file we define (will not overwrite already existing folders)
3. downloads glass lewis research, renames, and saves in correct folder
4. downloads the ballot list print page, renames, and saves in correct folder
5. downloads printed ballot page pdf from PE, renames, and saves in correct folder
6. the code that downloads the 3 reports also saves down timestamped logs in the company folder’s root directory so that we can review any securities that error out during run


![image](https://user-images.githubusercontent.com/48654156/178109156-6334ac47-06ad-4722-a26f-391a5c8f2779.png)


To Do: 
- update default download location
  - enables other users to use code easier
- update code to check for meetings before running
  - seperate out functions so that they only complete one item 
- remove hard coded PATHs
  - research ways to do this
- update logging to be more efficient 
