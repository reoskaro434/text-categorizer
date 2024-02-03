import re
import tkinter as tk
from tkinter import ttk
import sys
import tensorflow as tf
from nltk import word_tokenize
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import gensim.downloader as api
import numpy as np
import pickle


class ConsoleOutput:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')

    def flush(self):
        pass

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self._create_app()

        with open('tc_labels.pkl', 'rb') as file:
            self.loaded_label_names = pickle.load(file)

        nltk.download('punkt')  
        nltk.download('stopwords')
        self.stop_words = stopwords.words('english')
        self.lemmatizer = WordNetLemmatizer()

        self.glove = api.load("glove-twitter-25")

    def _create_app(self):
        self.title('Text Categorizer')

        self.text_entry = tk.Text(self, height=10)
        self.text_entry.pack(pady=10)

        self.variable = tk.StringVar(self)
        self.variable.set(None) # domyślna wartość
        self.dropdown = ttk.OptionMenu(self, self.variable, 'Wybierz opcję')
        self.dropdown.pack(pady=10)

        self.console = tk.Text(self, height=10, state='disabled')
        self.console.pack(pady=10)

        sys.stdout = ConsoleOutput(self.console)

        print_button = tk.Button(self, text='Categorize', command=self.categorize)
        print_button.pack(pady=10)

        clear_button = tk.Button(self, text='Clear Output', command=self.clear_console)
        clear_button.pack(side=tk.LEFT, padx=(5, 10), pady=10)
    def replace_if_number(self, word):
        if bool(re.match(r'^\d+$', word)):
            return 'number'
        
        if bool(re.search(r'\d', word)): # Mixed such as 33m
            return 'number'

        return word

    def apply_word2vec_model(self, word):
        # Check if the word exists in the model's vocabulary
        if word in self.glove:
            return self.glove[word]
        
        return self.glove['unknown']

    def clear_console(self):
        self.console.configure(state='normal')
        self.console.delete(1.0, tk.END)
        self.console.configure(state='disabled')

    def categorize(self):
        text = self.text_entry.get('1.0', 'end-1c')

        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        word_arr = word_tokenize(text)
        token_arr_no_stopwords = [ word for word in word_arr if word not in self.stop_words]
        lemmatized_token_arr = [ self.lemmatizer.lemmatize(word) for word in token_arr_no_stopwords ]
        replace_if_number_arr = [self.replace_if_number(lem) for lem in lemmatized_token_arr]
        apply_word2vec_model_arr = [self.apply_word2vec_model(lem) for lem in replace_if_number_arr]
        

        # Stack vectors into a single numpy array
        glove_array = np.vstack(apply_word2vec_model_arr)

        glove_array = np.array(glove_array).flatten()

        if len(glove_array) > 1100:
            raise ValueError('text is too large' + len(glove_array))
        desired_length = 1100

        glove_vector_padded = np.pad(glove_array, (0, desired_length - len(glove_array)), 'constant')
        # print(glove_vector_padded)
        # model = tf.keras.models.load_model('./saved_models/rnn_gru_3')
        model = tf.keras.models.load_model('C:/Users/reosk/projects/text-categorizer/saved_models/rnn_gru_3')

        glove_vector_padded_reshaped = glove_vector_padded.reshape(-1, 44, 25)

        predictions = model.predict(glove_vector_padded_reshaped)
        # print(predictions) # Dziala ale dostajemy liczby. trzeba zmienic na tagi

        percent_predictions = predictions[0] * 100

        for label, percentage in zip(self.loaded_label_names, percent_predictions):
            print(f"{label}: {percentage:.2f}%")
        

# Uruchomienie aplikacji
app = App()
app.mainloop()
