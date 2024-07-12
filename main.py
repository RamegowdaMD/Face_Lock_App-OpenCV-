
import os.path
import datetime
import subprocess
import tkinter as tk    
import cv2
from PIL import Image, ImageTk
import util
class App:
    def __init__(self):
        

        self.main_window = tk.Tk(className='FaceApp')

        self.main_window.geometry("850x500+250+100")
        self.main_window.configure(bg='#616161')

         

        self.text_label_main_window = util.get_text_label(self.main_window, 'FACE LOCK APP')
        self.text_label_main_window.place(x=320, y=20)

        self.login_button_main_window = util.get_button(self.main_window, 'LOGIN', 'green', self.login)
        self.login_button_main_window.place(x=450, y=150)
        self.register_new_user_button_main_window = util.get_button(self.main_window, 'REGISTER NEW USER', '#4169E1',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=450, y=250)
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=80, width=400, height=400)
        self.add_webcam(self.webcam_label)
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
        self.log_path = './log.txt'
    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        self._label = label
        self.process_webcam()
    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = './.tmp.jpg'

        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        
        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        name = output.split(',')[1][:-3]
        print(output)
        print(name) 
        x=len(name)
        
        var=name[:x-2]
        print(var)

        if  var in ['unknown_person', 'no_persons_found']:
            util.msg_box('Oops...', 'Unknown user. Please register new user or try again.')
        else:
            util.msg_box('Welcome back !', 'Welcome, {}.'.format(var))
            with open(self.log_path, 'a') as f:
                f.write('{},{}\n\n'.format(var, datetime.datetime.now()))
                f.close()

        os.remove(unknown_img_path)

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)

        self.register_new_user_window.geometry("850x500+250+100")

        self.register_new_user_window.configure(bg='#616161')
    
        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'REGISTRATION PAGE')
        self.text_label_register_new_user.place(x=300, y=20)

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'CONFIRM', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=450, y=250)
        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', '#4169E1', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=450, y=350)
        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=80, width=400, height=400)
        self.add_img_to_label(self.capture_label)
        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=450, y=180)
        
        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'ENTER YOUR NAME:')
        self.text_label_register_new_user.place(x=450, y=130)
    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()
    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture = self.most_recent_capture_arr.copy()
    def start(self):
        self.main_window.mainloop()
    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)
        
        util.msg_box('Success!', 'User was registered successfully !')

        self.register_new_user_window.destroy()
if __name__ == "__main__":
    app = App()
    app.start() 
