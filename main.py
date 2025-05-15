# Imports
import tkinter as tk
from tkinter import ttk, filedialog
import time
import math
import psycopg2
import os
from dotenv import load_dotenv
from typing import *


load_dotenv()

class iPhoneStartupAnimation:
    def __init__(self, root):
        self.loggedInUser = None
        self.root = root
        
        self.root.title("Sustaina")
        
        self.width = 390
        self.height = 844
        
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(False, False)
        
        self.bgColor = "#FFFFFF"
        self.accentColor = "#34C759"
        self.textColor = "#000000"
        
        self.mainFrame = tk.Frame(root, bg=self.bgColor)
        self.mainFrame.place(x=0, y=0, width=self.width, height=self.height)
        
        self.animationCanvas = tk.Canvas(self.mainFrame, bg=self.bgColor, highlightthickness=0)
        self.animationCanvas.place(x=0, y=0, width=self.width, height=self.height)
        self.animations = []
        
        self.tabFrames = []

        # anim delay
        self.root.after(2000, self.startAnimation)

        self.DBConnection()

    # connect to the database
    def DBConnection(self) -> None:
        """Connect to the database"""
        try:
            databaseURL = os.getenv("DATABASE_URL")
            self.conn = psycopg2.connect(databaseURL, sslmode='require')
            self.cur = self.conn.cursor()
            self.createTable()
        except Exception as e:
            print("Database connection error:", e)

    def createTable(self) -> None:
        """Creates the table to organize the data"""
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS clothes (
                id SERIAL PRIMARY KEY,
                name TEXT,
                description TEXT,
                score INT CHECK(score BETWEEN 1 AND 10),
                imagePath TEXT
            )
        ''')
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                description TEXT,
                imagePath TEXT
            )
        ''')
        self.conn.commit()
        
    def showLoginScreen(self):
        """Show login screen"""
        self.clearContent()
        frame = tk.Frame(self.mainContent, bg=self.bgColor)
        frame.pack(pady=50)

        tk.Label(frame, text="Login", font=("SF Pro", 20, "bold"), bg=self.bgColor).pack(pady=10)
        
        self.login_username = tk.StringVar()
        self.login_password = tk.StringVar()

        tk.Entry(frame, textvariable=self.login_username, font=("SF Pro", 14), width=30).pack(pady=5)
        tk.Entry(frame, textvariable=self.login_password, font=("SF Pro", 14), width=30, show="*").pack(pady=5)

        tk.Button(frame, text="Login", command=self.handleLogin, bg=self.accentColor, fg="white").pack(pady=10)
        tk.Button(frame, text="Sign Up", command=self.showSignupScreen, fg=self.textColor).pack()

    def showSignupScreen(self):
        """Show signup screen"""
        self.clearContent()
        frame = tk.Frame(self.mainContent, bg=self.bgColor)
        frame.pack(pady=50)

        tk.Label(frame, text="Sign Up", font=("SF Pro", 20, "bold"), bg=self.bgColor).pack(pady=10)

        self.signup_username = tk.StringVar()
        self.signup_password = tk.StringVar()
        self.signup_description = tk.StringVar()

        tk.Entry(frame, textvariable=self.signup_username, font=("SF Pro", 14), width=30).pack(pady=5)
        tk.Entry(frame, textvariable=self.signup_password, font=("SF Pro", 14), width=30, show="*").pack(pady=5)
        tk.Entry(frame, textvariable=self.signup_description, font=("SF Pro", 14), width=30).pack(pady=5)

        tk.Button(frame, text="Sign Up", command=self.handleSignup, bg=self.accentColor, fg="white").pack(pady=10)
        tk.Button(frame, text="Back to Login", command=self.showLoginScreen, fg=self.textColor).pack()

    def handleLogin(self):
        username = self.login_username.get()
        password = self.login_password.get()
        if self.login(username, password):
            self.showMainInterface()
        else:
            tk.messagebox.showerror("Error", "Invalid credentials")

    def handleSignup(self):
        username = self.signup_username.get()
        password = self.signup_password.get()
        description = self.signup_description.get()
        if not username or not password:
            tk.messagebox.showerror("Error", "Username and Password are required")
            return
        if self.signup(username, password, description):
            tk.messagebox.showinfo("Success", "Account created successfully!")
            self.showLoginScreen()
        else:
            tk.messagebox.showerror("Error", "Username already exists")
        
    def signup(self, username, password, description="", imagePath=""):
        try:
            self.cur.execute("INSERT INTO users (username, password, description, imagePath) VALUES (%s, %s, %s, %s)",
                            (username, password, description, imagePath))
            self.conn.commit()
            return True
        except Exception as e:
            print("Signup error:", e)
            return False

    def login(self, username, password):
        self.cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = self.cur.fetchone()
        if user:
            self.loggedInUser = {
                "id": user[0],
                "username": user[1],
                "description": user[3],
                "imagePath": user[4]
            }
            return True
        return False


    def startAnimation(self) -> None:
        """Starts the animation process"""
        self.drawLeafAnimation()
        self.processAnims()

    def processAnims(self) -> None:
        """Processes the animations"""
        if self.animations:
            removeAnims = []
            for animation in self.animations:
                animation["frame"] += 1
                animation["function"](animation["frame"], animation["max_frames"])
                if animation["frame"] >= animation["max_frames"]:
                    removeAnims.append(animation)
            for anim in removeAnims:
                self.animations.remove(anim)
        if self.animations:
            self.root.after(16, self.processAnims)

    def drawLeafAnimation(self) -> None:
        """Draws the leaf animation"""
        leafColor = self.accentColor
        leafSize = 80
        centerX = self.width // 2
        centerY = self.height // 2 - 50
        leafPoints = []
        for i in range(40):
            angle = math.radians(i * 9)
            r = leafSize * (1 + math.sin(angle)) / 3
            x = centerX + r * math.cos(angle)
            y = centerY + r * math.sin(angle)
            leafPoints.append((x, y))
        leafOutline = None

        def animateLeafDraw(frame: int, maxFrames: int) -> None:
            """Animates the drawing of the leaf outline.

            Args:
                frame (int): The current frame
                maxFrames (int): The maximum frames
            """
            nonlocal leafOutline
            if leafOutline:
                self.animationCanvas.delete(leafOutline)
            progress = min(1.0, frame / (maxFrames * 0.8))
            pointsToRender = int(len(leafPoints) * progress)
            if pointsToRender >= 2:
                leafOutline = self.animationCanvas.create_line(
                    *[coord for point in leafPoints[:pointsToRender] for coord in point],
                    fill=leafColor, width=3, smooth=True
                )
            if frame == maxFrames:
                self.animateLeafFill(leafSize)
        self.addAnimation(animateLeafDraw, 45)

    def animateLeafFill(self, leafSize: int) -> None:
        """Animate the filling of the leaf

        Args:
            leafSize (int): The size of the leaf (80)
        """
        centerX = self.width // 2
        centerY = self.height // 2 - 50
        leafPolygon = None

        def animateLeafFilling(frame: int, maxFrames: int) -> None:
            """Animate the filling of the leaf

            Args:
                frame (int): Current frame
                maxFrames (int): Maximum frame
            """
            nonlocal leafPolygon
            if leafPolygon:
                self.animationCanvas.delete(leafPolygon)
            progress = frame / maxFrames
            fillColor = self.hex_to_rgb(self.accentColor)
            alpha = int(255 * progress)
            fillColorWithAlpha = f"#{fillColor[0]:02x}{fillColor[1]:02x}{fillColor[2]:02x}"
            points = []
            for i in range(40):
                angle = math.radians(i * 9)
                r = leafSize * (1 + math.sin(angle)) / 3
                x = centerX + r * math.cos(angle)
                y = centerY + r * math.sin(angle)
                points.extend([x, y])
            leafPolygon = self.animationCanvas.create_polygon(
                points, fill=fillColorWithAlpha, outline=self.accentColor, width=2, smooth=True
            )
            if frame == maxFrames:
                self.animateShirt()
        self.addAnimation(animateLeafFilling, 30)

    def animateShirt(self) -> None:
        """Animate the shirt"""
        centerX = self.width // 2
        centerY = self.height // 2 + 50
        shirtWidth = 100
        shirtHeight = 80
        collarLeft = centerX - shirtWidth/4
        collarRight = centerX + shirtWidth/4
        slvLeftOut = centerX - shirtWidth/2
        slvLeftIn = centerX - shirtWidth/4
        slvRightOut = centerX + shirtWidth/2
        slvRightIn = centerX + shirtWidth/4
        bottomLeft = centerX - shirtWidth/3
        bottomRight = centerX + shirtWidth/3
        topY = centerY - shirtHeight/2
        sleeveY = centerY - shirtHeight/3
        bottomY = centerY + shirtHeight/2
        shirtOutline = None

        def animateShirtDraw(frame: int, maxFrames: int) -> None:
            """The shirt drawing animation.

            Args:
                frame (int): Current frame
                maxFrames (int): The maximum frame
            """
            nonlocal shirtOutline
            if shirtOutline:
                self.animationCanvas.delete(shirtOutline)
            progress = min(1.0, frame / (maxFrames * 0.8))
            segments = [
                (slvLeftOut, sleeveY, slvLeftIn, topY),
                (slvLeftIn, topY, collarLeft, topY),
                (collarLeft, topY, collarRight, topY),
                (collarRight, topY, slvRightIn, topY),
                (slvRightIn, topY, slvRightOut, sleeveY),
                (slvRightOut, sleeveY, slvRightOut, sleeveY + shirtHeight/5),
                (slvRightOut, sleeveY + shirtHeight/5, bottomRight, bottomY),
                (bottomRight, bottomY, bottomLeft, bottomY),
                (bottomLeft, bottomY, slvLeftOut, sleeveY + shirtHeight/5),
                (slvLeftOut, sleeveY + shirtHeight/5, slvLeftOut, sleeveY)
            ]
            totalSegments = len(segments)
            segmentsToRender = int(totalSegments * progress)
            for i in range(segmentsToRender):
                self.animationCanvas.create_line(
                    segments[i], fill="#007AFF", width=3, smooth=True
                )
            if frame == maxFrames:
                self.animateShirtFill()
        self.addAnimation(animateShirtDraw, 60)

    def animateShirtFill(self) -> None:
        """Fill the shirt in"""
        centerX = self.width // 2
        centerY = self.height // 2 + 50
        shirtWidth = 100
        shirtHeight = 80
        collarLeft = centerX - shirtWidth/4
        collarRight = centerX + shirtWidth/4
        slvLeftOut = centerX - shirtWidth/2
        slvLeftIn = centerX - shirtWidth/4
        slvRightOut = centerX + shirtWidth/2
        slvRightIn = centerX + shirtWidth/4
        bottomLeft = centerX - shirtWidth/3
        bottomRight = centerX + shirtWidth/3
        topY = centerY - shirtHeight/2
        sleeveY = centerY - shirtHeight/3
        bottomY = centerY + shirtHeight/2
        shirtPoints = [
            slvLeftOut, sleeveY,
            slvLeftIn, topY,
            collarLeft, topY,
            collarRight, topY,
            slvRightIn, topY,
            slvRightOut, sleeveY,
            slvRightOut, sleeveY + shirtHeight/5,
            bottomRight, bottomY,
            bottomLeft, bottomY,
            slvLeftOut, sleeveY + shirtHeight/5,
            slvLeftOut, sleeveY
        ]
        shirtPolygon = None

        def animateShirtFilling(frame: int, maxFrames: int) -> None:
            """Anime the shirt filling

            Args:
                frame (int): The current fram
                maxFrames (int): The maximum frame
            """
            nonlocal shirtPolygon
            if shirtPolygon:
                self.animationCanvas.delete(shirtPolygon)
            fillColor = self.hex_to_rgb("#007AFF")
            fillColorWithAlpha = f"#{fillColor[0]:02x}{fillColor[1]:02x}{fillColor[2]:02x}"
            shirtPolygon = self.animationCanvas.create_polygon(
                shirtPoints, fill=fillColorWithAlpha, outline="#007AFF", width=2, smooth=True
            )
            if frame == maxFrames:
                self.animateTextAppear()
        self.addAnimation(animateShirtFilling, 30)

    def animateTextAppear(self) ->  None:
        """Animate the text appearing"""
        centerX = self.width // 2
        centerY = self.height // 2 + 150
        textObject = None

        def animateText(frame: int, maxFrames: int) -> None:
            """Animate the sustaina text

            Args:
                frame (int): The current frame
                maxFrames (int): The maximum frame
            """
            nonlocal textObject
            if textObject:
                self.animationCanvas.delete(textObject)
            progress = frame / maxFrames
            scale = 0.5 + 0.5 * progress
            opacity = int(255 * progress)
            fontSize = int(36 * scale)
            textObject = self.animationCanvas.create_text(
                centerX, centerY,
                text="Sustaina",
                font=("SF Pro", fontSize, "bold"),
                fill=f"#{opacity:02x}{opacity:02x}{opacity:02x}"
            )
            if frame == maxFrames:
                self.root.after(1000, self.showMainInterface)
        self.addAnimation(animateText, 45)

    def showMainInterface(self) -> None:
        self.animationCanvas.delete("all")
        self.createStatusBar()
        self.createHomeIndicator()
        self.createBottomNav()
        self.updateTime()
        self.mainContent = tk.Frame(self.mainFrame, bg=self.bgColor)
        self.mainContent.place(x=0, y=45, width=self.width, height=self.height - 125)
        self.showHomeTab()

    # ui components
    def createStatusBar(self) -> None:
        """Create the status bar"""
        self.statusBar = tk.Frame(self.mainFrame, bg=self.bgColor, height=45)
        self.statusBar.place(x=0, y=0, width=self.width)
        self.timeLabel = tk.Label(self.statusBar, text="9:41", font=("SF Pro", 14, "bold"), bg=self.bgColor,
                                  fg=self.textColor)
        self.timeLabel.place(x=self.width // 2, y=15, anchor="center")

        self.batteryCanvas = tk.Canvas(self.statusBar, width=30, height=15, bg=self.bgColor, highlightthickness=0)
        self.batteryCanvas.place(x=self.width - 40, y=15, anchor="center")
        self.batteryCanvas.create_rectangle(1, 3, 25, 12, outline=self.textColor)
        self.batteryCanvas.create_rectangle(25, 5, 28, 10, fill=self.textColor, outline=self.textColor)
        self.batteryCanvas.create_rectangle(3, 5, 23, 10, fill=self.textColor, outline="")

        self.signalStrengthCanvas = tk.Canvas(self.statusBar, width=30, height=15, bg=self.bgColor,
                                              highlightthickness=0)
        self.signalStrengthCanvas.place(x=30, y=15, anchor="center")
        for i in range(4):
            height = 3 + i * 2
            self.signalStrengthCanvas.create_rectangle(i * 5, 15 - height, i * 5 + 3, 15, fill=self.textColor)

        self.wifiCanvas = tk.Canvas(self.statusBar, width=18, height=15, bg=self.bgColor, highlightthickness=0)
        self.wifiCanvas.place(x=70, y=15, anchor="center")
        for i in range(3):
            radius = 10 - i * 4
            x, y = 9, 12
            self.wifiCanvas.create_arc(x - radius, y - radius, x + radius, y + radius,
                                       start=45, extent=90, style="arc", outline=self.textColor, width=2)

    def createHomeIndicator(self) -> None:
        """Home indicator"""
        self.homeIndicator = tk.Frame(self.mainFrame, bg=self.textColor, height=5, width=120)
        self.homeIndicator.place(x=self.width // 2, y=self.height - 10, anchor="center")
        self.homeIndicator.config(bd=0, relief=tk.FLAT)
        self.homeIndicator.bind("<Button-1>", self.homeIndicatorPressed)

    def homeIndicatorPressed(self, event) -> None:
        """Is the home indicator pressed

        Args:
            event (Any): The data passed by the tkinter event
        """
        print(event)
        self.animateHomeIndicator()

    def animateHomeIndicator(self) -> None:
        """Home indicator animation"""
        initialWidth = 120
        targetWidth = 140

        def animate(frame, maxFrames):
            progress = frame / maxFrames
            if progress <= 0.5:
                currentWidth = initialWidth + (targetWidth - initialWidth) * (progress * 2)
            else:
                currentWidth = targetWidth - (targetWidth - initialWidth) * ((progress - 0.5) * 2)
            self.homeIndicator.config(width=int(currentWidth))
            if frame < maxFrames:
                self.root.after(16, lambda: animate(frame + 1, maxFrames))

        animate(0, 15)

    def createBottomNav(self) -> None:
        """Bottom navigation bar"""
        self.bottomNav = tk.Frame(self.mainFrame, bg="#F2F2F7", height=80)
        self.bottomNav.place(x=0, y=self.height - 80, width=self.width)
        navItems = ["Home", "Search", "Upload", "Profile"]
        navSymbols = ["H", "S", "U", "P"]

        for i in range(4):
            tabFrame = tk.Frame(self.bottomNav, bg="#F2F2F7", width=self.width // 4, height=80)
            tabFrame.pack(side=tk.LEFT)
            tabFrame.pack_propagate(False)
            self.tabFrames.append(tabFrame)

            iconCircle = tk.Canvas(tabFrame, width=50, height=50, bg="#F2F2F7", highlightthickness=0)
            iconCircle.place(relx=0.5, rely=0.4, anchor="center")
            iconCircle.create_oval(5, 5, 45, 45, fill=self.accentColor if i == 0 else "#F2F2F7", outline="")

            if i == 0:
                iconLabel = tk.Label(iconCircle, text=navSymbols[i], font=("SF Pro", 18, "bold"), fg="white",
                                     bg=self.accentColor)
            else:
                iconLabel = tk.Label(iconCircle, text=navSymbols[i], font=("SF Pro", 18), fg=self.textColor,
                                     bg="#F2F2F7")
            iconLabel.place(relx=0.5, rely=0.5, anchor="center")

            itemLabel = tk.Label(tabFrame, text=navItems[i], font=("SF Pro", 12),
                                 fg=self.accentColor if i == 0 else "#8E8E93", bg="#F2F2F7")
            itemLabel.place(relx=0.5, rely=0.75, anchor="center")

            tabFrame.bind("<Button-1>", lambda e, idx=i: self.tabPressed(idx))
            iconCircle.bind("<Button-1>", lambda e, idx=i:self.tabPressed(idx))
            iconLabel.bind("<Button-1>", lambda e, idx=i: self.tabPressed(idx))
            itemLabel.bind("<Button-1>", lambda e, idx=i: self.tabPressed(idx))

    def tabPressed(self, index: int) -> None:
        """Choose the tab pressed

        Args:
            index (int): The index of the tab pressed
        """
        for i, tabFrame in enumerate(self.tabFrames):
            iconCanvas = None
            itemLabel = None
            for widget in tabFrame.winfo_children():
                if isinstance(widget, tk.Canvas):
                    iconCanvas = widget
                    iconCanvas.delete("all")
                    iconCanvas.create_oval(5, 5, 45, 45, fill=self.accentColor if i == index else "#F2F2F7", outline="")
                elif isinstance(widget, tk.Label) and widget.cget("text") in ["Home", "Search", "Upload", "Profile"]:
                    itemLabel = widget
                    itemLabel.config(fg=self.accentColor if i == index else "#8E8E93")
            if iconCanvas:
                for innerWidget in iconCanvas.winfo_children():
                    if isinstance(innerWidget, tk.Label):
                        innerWidget.config(bg=self.accentColor if i == index else "#F2F2F7",
                                           fg="white" if i == index else self.textColor)

        self.switchTab(index)
        self.animateTabSelection(index)
        
    def uploadImage(self) -> str:
        filetypes = [('Image Files', '*.png *.jpg *.jpeg *.gif')]
        filepath = filedialog.askopenfilename(title='Choose Image', filetypes=filetypes)
        return filepath

    def switchTab(self, index: int) -> None:
        """Switches the tab

        Args:
            index (int): The current index of the tab
        """
        self.clearContent()
        if index == 0:
            self.showHomeTab()
        elif index == 1:
            self.showSearchTab()
        elif index == 2:
            self.showUploadTab()
        elif index == 3:
            self.showProfileTab()

    def animateTabSelection(self, index: int) -> None:
        """Animate the tab selection

        Args:
            index (int): The index of the tab
        """
        frames = 10
        tabFrame = self.tabFrames[index]
        iconCanvas = None
        for widget in tabFrame.winfo_children():
            if isinstance(widget, tk.Canvas):
                iconCanvas = widget
                break
        if not iconCanvas:
            return

        def animate(frame, maxFrames: int) -> None:
            """Animates the tab selection

            Args:
                frame (int): The current frame
                maxFrames (int): The maximum frames
            """
            progress = frame / maxFrames
            if progress <= 0.5:
                scale = 1.0 + 0.2 * (progress * 2)
            else:
                scale = 1.2 - 0.2 * ((progress - 0.5) * 2)
            size = int(50 * scale)
            offset = int((50 - size) / 2)
            iconCanvas.delete("all")
            iconCanvas.create_oval(offset, offset, size + offset, size + offset, fill=self.accentColor, outline="")
            for child in iconCanvas.winfo_children():
                if isinstance(child, tk.Label):
                    fontSize = int(18 * scale)
                    child.config(font=("SF Pro", fontSize, "bold"))
            if frame < maxFrames:
                self.root.after(16, lambda: animate(frame + 1, maxFrames))

        animate(0, frames)

    def updateTime(self) -> None:
        """_summary_
        """
        currentTime = time.strftime("%I:%M")
        if currentTime.startswith("0"):
            currentTime = currentTime[1:]
        self.timeLabel.config(text=currentTime)
        self.root.after(1000, self.updateTime)

    def hex_to_rgb(self, hexColor: str) -> Tuple[int, int, int]:
        """Converts the hex code to rgb

        Args:
            hexColor (string): _description_

        Returns:
            Tuple: The tuple of the rgb values
        """
        hexColor = hexColor.lstrip('#')
        return tuple(int(hexColor[i:i+2], 16) for i in (0, 2, 4))

    def addAnimation(self, function: object, maxFrames: int) -> None:
        """Adds the animation to the list

        Args:
            function (object): The current action
            maxFrames (int): The maximum frames
        """
        self.animations.append({
            "function": function,
            "frame": 0,
            "max_frames": maxFrames
        })

    def clearContent(self) -> None:
        """Clears the content of the main content area
        """
        for widget in self.mainContent.winfo_children():
            widget.destroy()

    def showHomeTab(self) -> None:
        """_summary_
        """
        label = tk.Label(self.mainContent, text="Welcome to Sustaina!", font=("SF Pro", 18), bg=self.bgColor,
                         fg=self.textColor)
        label.pack(pady=20)
        
    def showProfileTab(self):
        self.clearContent()
        frame = tk.Frame(self.mainContent, bg=self.bgColor)
        frame.pack(fill=tk.BOTH, expand=True)

        if not self.loggedInUser:
            tk.Label(frame, text="You're not logged in.", font=("SF Pro", 16), bg=self.bgColor).pack(pady=20)
            tk.Button(frame, text="Login", command=self.showLoginScreen, bg=self.accentColor, fg="white").pack()
            return

        tk.Label(frame, text=f"Username: {self.loggedInUser['username']}", font=("SF Pro", 16), bg=self.bgColor).pack(pady=10)
        tk.Label(frame, text=f"Description: {self.loggedInUser['description'] or 'N/A'}", bg=self.bgColor).pack(pady=5)

        if self.loggedInUser['imagePath']:
            try:
                img = tk.PhotoImage(file=self.loggedInUser['imagePath'])
                imgLabel = tk.Label(frame, image=img, bg=self.bgColor)
                imgLabel.image = img  # Keep reference
                imgLabel.pack(pady=10)
            except Exception as e:
                tk.Label(frame, text="Error loading profile image", fg="red", bg=self.bgColor).pack()
        else:
            tk.Label(frame, text="No profile picture set", bg=self.bgColor).pack()

        def chngProfilePic():
            path = self.uploadImage()
            if path:
                self.cur.execute("UPDATE users SET imagePath=%s WHERE id=%s", (path, self.loggedInUser['id']))
                self.conn.commit()
                self.loggedInUser['imagePath'] = path
                self.showProfileTab()

        tk.Button(frame, text="Change Profile Picture", command=chngProfilePic, bg="#50C878", fg="white").pack(pady=10)
        tk.Button(frame, text="Logout", command=self.logout, bg="#FF6347", fg="white").pack(pady=5)

    def logout(self):
        self.loggedInUser = None
        self.showLoginScreen()
        

    def uploadImage(self) -> str:
        """Uplad the image

        Returns:
            filepath: The file path of the image
        """
        filetypes = [('Image Files', '*.png *.jpg *.jpeg *.gif')]
        filepath = filedialog.askopenfilename(title='Choose Image', filetypes=filetypes)
        return filepath

    def showUploadTab(self) -> None:
        """Show the upload section contents
        """
        self.name_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.score_var = tk.StringVar()
        self.imagePath = ""

        tk.Label(self.mainContent, text="Clothing Name", font=("SF Pro", 14), bg=self.bgColor).pack(pady=5)
        tk.Entry(self.mainContent, textvariable=self.name_var, font=("SF Pro", 12)).pack(pady=5, padx=20, fill=tk.X)

        tk.Label(self.mainContent, text="Description", font=("SF Pro", 14), bg=self.bgColor).pack(pady=5)
        tk.Entry(self.mainContent, textvariable=self.desc_var, font=("SF Pro", 12)).pack(pady=5, padx=20, fill=tk.X)

        tk.Label(self.mainContent, text="Sustainability Score (1–10)", font=("SF Pro", 14), bg=self.bgColor).pack(pady=5)
        ttk.Combobox(self.mainContent, textvariable=self.score_var, values=[str(i) for i in range(1, 11)]).pack(
            pady=5, padx=20, fill=tk.X)

        self.imageLabel = tk.Label(self.mainContent, text="No image selected", font=("SF Pro", 12), bg=self.bgColor,
                             fg="#888")
        self.imageLabel.pack(pady=5, padx=20, fill=tk.X)

        def choose_img():
            self.imagePath = self.uploadImage()
            self.imageLabel.config(text=self.imagePath.split("/")[-1] if self.imagePath else "No image selected")

        tk.Button(self.mainContent, text="Choose Image", command=choose_img).pack(pady=5)
        tk.Button(self.mainContent, text="Upload", command=self.saveToDB, bg=self.accentColor, fg="white").pack(pady=10)

    def saveToDB(self) -> None:
        """Save the data to the database
        """
        name = self.name_var.get()
        desc = self.desc_var.get()
        score = self.score_var.get()
        imagePath = self.imagePath

        if not all([name, desc, score, imagePath]):
            print("All fields are required.")
            return

        try:
            self.cur.execute(
                "INSERT INTO clothes (name, description, score, imagePath) VALUES (%s, %s, %s, %s)",
                (name, desc, int(score), imagePath)
            )
            self.conn.commit()
            print("Saved to database!")
        except Exception as e:
            print("Error saving:", e)

    def showSearchTab(self) -> None:
        """Show the search tab contents
        """
        self.searchVariable = tk.StringVar()
        self.filterVariable = tk.StringVar()

        searchEntry = tk.Entry(self.mainContent, textvariable=self.searchVariable, font=("SF Pro", 14))
        searchEntry.pack(pady=10, padx=20, fill=tk.X)

        filterDropdown = ttk.Combobox(self.mainContent, textvariable=self.filterVariable,
                                       values=[str(i) for i in range(1, 11)])
        filterDropdown.set("Filter by Score")
        filterDropdown.pack(pady=10, padx=20, fill=tk.X)

        searchButton = tk.Button(self.mainContent, text="Search", command=self.searchFromDatabase)
        searchButton.pack(pady=5)

        self.resultsBox = tk.Text(self.mainContent, wrap=tk.WORD, font=("SF Pro", 12), height=10)
        self.resultsBox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    def searchFromDatabase(self) -> None:
        """Search the database with the query
        """
        self.resultsBox.delete(1.0, tk.END)
        name = self.searchVariable.get()
        score = self.filterVariable.get()

        query = "SELECT * FROM clothes WHERE TRUE"
        params = []

        if name:
            query += " AND name ILIKE %s"
            params.append(f"%{name}%")
        if score.isdigit():
            query += " AND score >= %s"
            params.append(score)

        try:
            self.cur.execute(query, params)
            results = self.cur.fetchall()
            for item in results:
                self.resultsBox.insert(tk.END, f"{item[1]} | {item[2]} | ⭐{item[3]}\n\n")
        except Exception as e:
            print("Search error:", e)


#driver code
if __name__ == "__main__":
    root = tk.Tk()
    app = iPhoneStartupAnimation(root)
    root.mainloop()