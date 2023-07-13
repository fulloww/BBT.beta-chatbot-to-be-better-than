
# Importing Libraries
import re
from nltk.corpus import wordnet
import nltk
nltk.download('all')
import itertools
import nltk

# List of Keywords
list_words=[
    'hello','bye',
    'suicide','kill','die','want','feel',
    'stupid','dumb','asshole',
    'think', 'was','thought','thinking'
    ]

list_syn={}
for word in list_words:
    synonyms=[]
    for syn in wordnet.synsets(word): # returns a set of synonyms that share a common meaning 
        for lem in syn.lemmas(): # returns the base form of the synonym (runner --> run)
            # Remove any special character
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem.name())
            synonyms.append(lem_name)
    list_syn[word]=set(synonyms)

# Building dictionary of Intents and Keywords
keywords={}
keywords_dict={}

# Creating a list of synonyms with multiple related words
new_list_syn_greetings = itertools.chain(list_syn['hello'], ['hey'])
new_list_syn_goodbyes = list_syn['bye']
new_list_syn_insult = itertools.chain(list_syn['stupid'], list_syn['dumb'], list_syn['asshole'])
new_list_syn_suicide = itertools.chain(list_syn['suicide'], list_syn['kill'], list_syn['die'])
new_list_syn_automaticThought = itertools.chain(list_syn['think'], list_syn['was'], list_syn['thought'], list_syn['thinking'])

list_keywords = {
    'greetings': new_list_syn_greetings,
    'goodbyes': new_list_syn_goodbyes,
    'insult': new_list_syn_insult,
    'suicide': new_list_syn_suicide, 
    'automaticThought': new_list_syn_automaticThought
    }

for keyword in list_keywords:
    keywords[keyword]=[]
    # Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
    for synonym in list(list_keywords[keyword]):
        # Formatting the synonym with RegEx metacharacters to make them visible to Regular Expression's search
        keywords[keyword].append('.*\\b'+synonym+'\\b.*') 

    for intent, keys in keywords.items():
        # Joining the values in the keywords dictionary with the OR (|) operator
        keywords_dict[intent]=re.compile('|'.join(keys))

# Building a dictionary of responses
responses={
    'greetings':'Hello! So, tell me how have you been feeling?',
    'suicide':'If you are feeling vulnerable and need help, Please call 112 or 914 590 055 to seek help.',
    'goodbyes':'Bye. Hope I\'ve been helpful.',
    'insult': 'Oh! that\'s mean :(',
    'automaticThought': 'When you were in that situation and that thought came to you, how did you feel?'
}

def get_response(msg):
    matched_intent = None 
    for intent,pattern in keywords_dict.items():
        # Searching for keywords from user input
        if re.search(pattern, msg): 
            # if a keyword matches, select the corresponding intent
            matched_intent = intent  
    
    if matched_intent in responses:
        key = matched_intent
        return responses[key]
    return 'none' # In this case the dialogue flow continues


# CHAT GUI

# In[ ]:


from tkinter import *
from nltk.sentiment import SentimentIntensityAnalyzer
import pickle

BG_GRAY = "#ABB2B9"
BG_COLOR = "white"
TEXT_COLOR = "black"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

bot_name = "BBT.beta"
script_answers = [ 
              "I’m sorry that you feel this way. Did anything in particular trigger this feeling?\
               \nPlease provide a detailed explanation of the situation.",
              "What were you thinking at the time?",
              "Please, Rate how intense this feeling was (1-100)",
              "What has happened to make you believe the thought is true?",
              "What evidence is there that this thought is not true?",
              "Taking the information into account, is there an alternative way of thinking about the situation? Please give an example",
              "How would you rate your mood now? (1-100)",
             ]
# List of the cognitive distortions 
CD = {
    'Always Being Right'        : 'DEFINITION: This way of thinking is characterized by a strong need or need to be right or to have other\
                                people affirm one\'s beliefs, opinions, or actions. It might make it difficult to consider different\
                                perspectives or to admit mistakes, which can pose problems in relationships and communication.\
                                \nLINK WITH TIPS:\nhttps://www.therapynowsf.com/blog/always-being-right-gearing-up-for-intellectual-battle',
    'Blaming'                   : 'DEFINITION: Attributing negative occurrences or events to someone or something else instead of accepting\
                                responsibility or taking into account the impact of one\'s own actions or beliefs is the cognitive distortion\
                                known as "blaming." Blaming can result in negative behaviors and emotions including rage, resentment, and avoidance.\
                                \nLINK WITH TIPS: \nhttps://www.vacounseling.com/blaming-cognitive-distortion/',
    'Catastrophizing'           :'DEFINITION: Predicting a negative outcome and jumping to the conclusion that if the negative outcome did\
                                in fact happen, it would be a catastrophe.\
                                \nLINK WITH TIPS: \nhttps://positivepsychology.com/catastrophizing/',
    'Control Fallacies'         : 'DEFINITION: The fallacy of control occurs when you believe you have too much power over a circumstance\
                                or your lot in life.\
                                \nLINK WITH TIPS: \nhttps://www.therapynowsf.com/blog/control-fallacies-delving-deeper-into-cognitive-distortions',
    'Emotional Reasoning'       : 'DEFINITION: When a person uses emotional reasoning, a cognitive distortion, they come to the\
                                conclusion that something\ is true regardless of the available evidence. Your thoughts are obscured\
                                by your emotions, and your reality is similarly obscured.\
                                \nLINK WITH TIPS: \nhttps://theeverygirl.com/17-of-the-easiest-ways-to-get-healthier-now/',
    'Fallacy Of Change'         : 'DEFINITION: This mental fallacy assumes that people ought to adapt to fit their own interests.\
                                The person will exert pressure on others to alter their behavior because they believe doing so\
                                will make them happier. They are convinced that changing a person is necessary for happiness.\
                                \nLINK WITH TIPS: \nhttps://www.therapynowsf.com/blog/the-fallacy-of-change-and-the-pursuit-of-happiness',
    'Fallacy Of Fairness'       : 'DEFINITION: The idea that fairness and equality should be the foundation of everything in life\
                                is known as the Fallacy of Fairness.\
                                \nhttps://www.therapynowsf.com/blog/the-fallacy-of-fairness-an-overview-of-this-cognitive-distortion',
    'Filtering'                 : 'DEFINITION: When we keep just the negative memories and the negative feelings associated with them,\
                                mental filtering takes place and we reject the positive recollections.\
                                \nLINK WITH TIPS: \nhttps://www.vacounseling.com/mental-filtering-cognitive-distortion/',
    'Global Labelling'          : 'DEFINITION: Labeling is a cognitive distortion in which we extrapolate from a single\
                                attribute of a person to that person as a whole.\
                                \nLINK WITH TIPS: \nhttps://courageousandmindful.com/overcoming-labeling-and-mislabeling-a-cognitive-distortion/',
    'Heaven\'s Reward Fallacy'  : 'DEFINITION: The distortion known as Heaven\'s Reward Fallacy is founded on the justification that your rewards\
                                should be determined by how hard you work.\
                                \nLINK WITH TIPS: \nhttps://cognitiontoday.com/heavens-reward-fallacy/',
    'Jumping to Conclusions'    : 'DEFINITION: Making arbitrary, negative assumptions about the thoughts of others or the future.\
                                \nLINK WITH TIPS: \
                                \nhttps://www.therapynowsf.com/blog/jumping-to-conclusions-learn-how-to-stop-making-anxiety-fueled-mental-leaps',
    'Overgeneralization'        : 'DEFINITION: A type of cognitive distortion called overgeneralization occurs when someone extrapolates\
                                information from one incident to all other events.\
                                \nLINK WITH TIPS: \nhttps://www.verywellmind.com/overgeneralization-3024614',
    'Personalization'           : 'DEFINITION: Personalization is the idea that something is totally your fault even when you had little\
                                to no influence on the outcome.\
                                \nLINK WITH TIPS: \nhttps://www.therapynowsf.com/blog/personalization-a-common-type-of-negative-thinking',
    'Polarized'                 : 'DEFINITION: This distortion, also known as "all-or-nothing" or "black-and-white thinking,"\
                                happens when people regularly think in extremes without taking all the relevant information into account.\
                                \nLINK WITH TIPS: \nhttps://exploringyourmind.com/polarized-thinking-cognitive-distortion/',
    'Shoulds'                   : 'DEFINITION: "Should" statements are irrational rules you make for yourself and others\
                                without taking into account the particulars of a situation.\
                                They are cognitive distortions. You tell yourself that there should be no exceptions to how things should be done.\
                                \nLINK WITH TIPS: \nhttps://www.therapynowsf.com/blog/should-statements-reframe-the-way-you-think'
} 

relaxation_exercise = "I have detected that your mood hasn't improved, so I recommend you to follow this link to do a relaxation\
                       exercise in order to improve your mood"\
                       + "\n" + "LINK TO DEEP BREATHING EXERCISE VIDEO: \nhttps://www.youtube.com/watch?v=tEmt1Znux58"             

class ChatGUI:
    
    def __init__(self):
        self.window = Tk()
        self.setup_main_window()
        self.msg_entry.delete(0, END)
        self.insert_kai_message("Hello!\
            \nMy name is BBT bot and I'm going to give you support to your self-directed CBT Therapy session.\
            \nSo, how have you been feeling?")
        self.step = 0 # Steps that indicate in which stage the therapy session is
        self.sia = SentimentIntensityAnalyzer()
        self.automatic_thougth = None
        self.cognitive_distortion = None
        self.pre_mood_rating = None
        self.post_mood_rating = None

    def run(self):
        self.window.mainloop()

    # Configures the main window of the interface    
    def setup_main_window(self):
        self.window.title("Chatbot to suppport Self-Directed CBT Therapy")
        self.window.resizable(width=False, height=False) # Make the size of the window static
        self.window.configure(width=1366, height=768, bg=BG_COLOR) # Configure size of the window
        
        # TOP LABEL
        head_label = Label(self.window, 
                           bg=BG_COLOR, 
                           fg=TEXT_COLOR, 
                           text="BBT", 
                           font=FONT_BOLD, 
                           pady=10)
        head_label.place(relwidth=1)
        
        # BOTTOM LABERL
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        # DIVIDER   
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        # TEXT WIDGET
        self.text_widget = Text(self.window, 
                                width=20,
                                height=2, 
                                bg=BG_COLOR, 
                                fg=TEXT_COLOR, 
                                font=FONT, 
                                padx=5, 
                                pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        # SCROLL BAR
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)
        
        # MESSAGE ENTRY
        self.msg_entry = Entry(bottom_label, bg="white", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self.on_enter_pressed)
        
        # SEND BUTTON
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY, command=lambda: self.on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
    
    # When the user presses enter (or sent), the user message is stored
    # and the user indetifier is then inserted into de chat
    def on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self.insert_message(msg, "You")
    
    # Inserts the message into the chat
    def insert_message(self, msg, sender):
        if not msg:
            return
        # Insert user message into chat    
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        
        # Insert chatbot message into chat
        if (self.step == 3 or self.step == 7): # Check mood rating
            self.insert_kai_message(self.check_rating(msg))
            #  Check wether the mood has improved
            if (self.step == 7 and (self.post_mood_rating - self.pre_mood_rating) >= 0):
                self.insert_kai_message(relaxation_exercise)
                self.step = 0
        else:
            kai_answer = get_response(msg)
            # Intent matched 
            if (kai_answer == 'Hello! So, tell me how have you been feeling?' or 
                kai_answer == 'Bye. Hope I\'ve been helpful.'):
                self.step = 0 # Resetting the dialoge flow
            # Intent not matched
            if (kai_answer == 'none'):
                # Checking if user's feeling is positive or negative
                if (self.step == 0 and self.sia.polarity_scores(msg)["compound"] > 0):
                    self.insert_kai_message("I'm glad that you feel this way :)")
                    self.step = 0
                    
                else:
                    # Getting the response from script to follow the dialogue flow of the therapy
                    self.insert_kai_message(script_answers[self.step])
                    if (self.step == 1): # Storing the potentniala automatic thought of the user
                        self.automatic_thought = msg
                    self.step = self.step + 1           
            else: 
                self.insert_kai_message(kai_answer)
                    
        self.text_widget.see(END)
          
    def insert_kai_message(self, msg):
        msg1 = f"{bot_name}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
    
    # Check that the user input is valid (a number between 1-100)
    def check_rating(self, msg):
        kai_answer = "Please enter a valid answer"
        if (msg.isnumeric()):
                rating = int(msg)
                if (rating >= 1 and rating <= 100):
                    if (self.step == 7):
                        kai_answer = self.detect_cognitive_distortion()
                        self.post_mood_rating = rating
                    else:
                        kai_answer = script_answers[self.step]
                        self.step += 1
                        self.pre_mood_rating = rating
        return kai_answer

    # Detect potential cognitive distortion with a ml model
    def detect_cognitive_distortion(self):
        pickled_model = pickle.load(open('cognitive_distortion_detector_model.pkl', 'rb'))
        self.cognitive_distortion = pickled_model.predict([self.automatic_thought])[0]
        if (self.cognitive_distortion != "NO"):
            msg = "I have detected a potential cognitive distortion: " + self.cognitive_distortion + "\n" + CD[self.cognitive_distortion]
            return msg
     
if __name__ == "__main__":
    app = ChatGUI()
    app.run()

