# SPOJ-Scraping
Extracts all the correct submissions of a user on SPOJ

spoj_solutions.py[1] file helps to save all the solved submissions. spoj_solutions_plain.py[2] has the same functioning. Just that the scraping is done from a different URL. [1] is done from URL: "http://www.spoj.com/files/src/[SubmissionID]/" and [2] is done from URL: "http://www.spoj.com/files/src/plain/[SubmissionID]/" which is a plaintext view of submitted codes.

One should add their username and password in `login_details` to make it work. All the codes will be saved in spoj_solutions folder, that will be created in currrent working directory. Comments are written in the code to make necessary changes and extract required codes.
