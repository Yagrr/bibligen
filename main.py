from app import App, UserInterface


def main():
    app = App()
    frame = UserInterface(app)
    app.mainloop()

if __name__ == "__main__":
    main()
