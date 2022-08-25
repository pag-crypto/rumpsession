import json
import os

#the name of the JSON file downloaded from HotCRP
RUMP_SESSION_JSON_FILE = "crypto2022rump-data.json"
#This is the order in which the accepted talks will appear in the PDF.
#This string was copy-pasted from an Excel spreadsheet; it gets converted to a list of numbers in the main method.
#Each of these PIDs is the submission ID from HotCRP.
#It also contains breaks interspersed throughout the talks.
pid_order_from_csv = """
11
10
21
5
6
7
2
Break
3
19
35
12
13
14
16
Break
20
8
23
24
27
25
Break
28
29
32
22
33
34
36
Break
17
18
26
31
15
"""

latex_preamble = ""



def make_break_slide(msg):
    print("\\begin{frame}")
    print("\centering\Huge "+msg)
    print("\end{frame}")
#Slides that list the next speaker's name, their title, and the name of the following speaker, so they can get ready to come up
def make_interstitial_slide(title, curr_author_names, next_author_names):
    print("\\begin{frame}")
    print("\centering\Huge "+title+"\\\\")
    print("\\begin{center}")
    print("\Large "+curr_author_names+"\\\\")
    print("\large Next up: "+next_author_names+"\\\\")
    print("\end{center}")
    print("\end{frame}")

def make_includepdf(fname):
    print("\includepdf[pages=-]{"+fname+"}")

#The prefix of the talk PDF name, downloaded from HotCRP
talkname_prefix = "crypto2022rump-paper"
finalname_prefix = "crypto2022rump-final"
DOT_PDF = ".pdf"
PREAMBLE_FILE = "preamble.txt"

#Assemble the LaTeX file, with \includepdf statements for
#the PDF slides of each PID in the (reformatted) pid_order_from_csv string
def make_rump_session(fname):
    with open(PREAMBLE_FILE, "r+") as preamble_file:
        latex_preamble = preamble_file.read()

    print(latex_preamble)
    data_string = None
    with open(fname, "r+") as datafile:
        data_string = datafile.read()

    submissions_list = json.loads(data_string)
    submission_dict_by_pid = dict()
    for submission in submissions_list:
        #print(submission['pid'])
        submission_dict_by_pid[str(submission['pid'])] = submission
        
    pid_order = pid_order_from_csv.replace("\n", ",")
    #"Come back at..." times for break slides
    break_list = ["20:20", "21:10", "22:00", "22:40"]
    break_counter = 0
    idx = 0
    #Get rid of first and last char becuse they were both commas
    pid_order = pid_order[1:-1].split(",")
    for pid in pid_order:
        if not (pid.lower() == "break" or pid == ''):
            #print()
            #authors = submission_dict_by_pid[""+pid]['authors']
            #print(authors)
            speaker_name = submission_dict_by_pid[""+pid]['speakers_name']
            if idx+1 == len(pid_order):
                next_speaker_name = "N/A"
            else:
                next_pid = pid_order[idx+1]
                if not next_pid == 'Break':
                    next_speaker_name = submission_dict_by_pid[next_pid]['speakers_name']
                else:
                    next_speaker_name = "Break"
            #Exception cases for the people who didn't write their full name as the "speaker name"
            if speaker_name == 'Me':
                speaker_name = "Jean-Jacques Quisquater"
                #print(submission_dict_by_pid[""+pid]['authors'])
            if speaker_name == 'Orr':
                speaker_name = "Orr Dunkelman"
            if next_speaker_name == 'Orr':
                next_speaker_name = 'Orr Dunkelman'
            #print(speaker_name+","+next_speaker_name)
            idx += 1
            #The replace statement in this line is to handle talks with titles that are LaTeX control characters
            make_interstitial_slide(submission_dict_by_pid[""+pid]['title'].replace("&", "\&"), speaker_name, next_speaker_name)
            #Decide whether to include the submitted slides or final slides or uploaded slides
            #We needed this because not everybody uploaded final slides, and some people uploaded final slides differently than others.
            submission_slides_fname = talkname_prefix+pid+DOT_PDF
            final_slides_fname = finalname_prefix+pid+DOT_PDF
            upload_slides_fname = ""+pid+"/slides.pdf"
            if os.path.exists(upload_slides_fname):
                include_fname = upload_slides_fname
            elif os.path.exists(final_slides_fname):
                include_fname = final_slides_fname
            else:
                include_fname = submission_slides_fname
            #PIDs of talks that should not have slides included.
            exclude_list = ['2']
            if not (pid in exclude_list):
                make_includepdf(include_fname)
                
        elif pid.lower() == "break":
            idx += 1
            #Insert slide that says break
            make_break_slide("BREAK\\\\ Come back at "+break_list[break_counter])
            break_counter = break_counter+1

    print("\\begin{frame}")
    print("\centering\Huge THE END!!!\\\\ Thank you to all the speakers!")
    print("\end{frame}")
    print("\end{document}")
    


if __name__=='__main__':
    make_rump_session(RUMP_SESSION_JSON_FILE)
    exit(0)
