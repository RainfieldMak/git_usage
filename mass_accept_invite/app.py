import tkinter as tk
from script import mass_accept

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Auto Accept Invite")

        self.frame = tk.Frame(self.root, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.header = self.HeaderLabel(self)
        self.tokenfield = self.TokenField(self)
        self.resultfield = self.ResultField(self)

    class HeaderLabel:
        def __init__(self, app):
            self.app = app
            self.label = tk.Label(self.app.frame, text="GitHub Auto Accept Invite", font=("Helvetica", 16), bg="white")
            self.label.pack(pady=10)

    class TokenField:
        def __init__(self, app):
            self.app = app
            self.token = None

            self.frame = tk.Frame(self.app.frame, bg="white")
            self.frame.pack(pady=20)

            self.label = tk.Label(self.frame, text="Enter GitHub Token", bg="white")
            self.label.pack(side=tk.LEFT, padx=(10, 5))

            self.entry = tk.Entry(self.frame, show="*")
            self.entry.pack(side=tk.LEFT, padx=(0, 10))

            self.button = tk.Button(self.app.frame, text="Accept Invite", command=self.get_text_entry)
            self.button.pack(pady=(0, 20))

        def get_token(self):
            return self.token

        def set_token(self, token):
            self.token = token


        def get_text_entry(self):
            
            entered_token = self.entry.get()
            self.set_token(entered_token)
            tool=mass_accept.tool(self.get_token())
            out=tool.accept_invite()

            for line in out:

                self.app.resultfield.update_text(line)

    class ResultField:
        def __init__(self, app):
            self.app = app

            self.out_frame = tk.Frame(self.app.frame, bg="white")
            self.out_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            self.out_scrollbar = tk.Scrollbar(self.out_frame)
            self.out_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.out = tk.Text(self.out_frame, bg="white", yscrollcommand=self.out_scrollbar.set)
            self.out.pack(fill=tk.BOTH, expand=True)

            self.out_scrollbar.config(command=self.out.yview)

        def update_text(self, text):
            self.out.insert(tk.END, text + "\n")

root = tk.Tk()
app = App(root)
root.mainloop()
