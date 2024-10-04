import tkinter as tk
from tkinter import ttk, messagebox
import time
from threading import Thread

class CommunicationSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Communication Model Simulator")
        
        # Create notebook (tab layout)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')
        
        # Request-Response Frame
        self.request_response_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.request_response_frame, text="Request-Response")
        
        # Publish-Subscribe Frame
        self.publish_subscribe_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.publish_subscribe_frame, text="Publish-Subscribe")
        
        # Setup each frame
        self.setup_request_response()
        self.setup_publish_subscribe()

    def setup_request_response(self):
        # Title
        ttk.Label(self.request_response_frame, text="Request-Response Simulation", font=("Arial", 14)).pack(pady=10)

        # Input for sending request
        self.request_input = ttk.Entry(self.request_response_frame, width=40)
        self.request_input.pack(pady=5)

        # Button to send request
        send_button = ttk.Button(self.request_response_frame, text="Send Request", command=self.send_request)
        send_button.pack(pady=10)

        # Label for server response
        self.response_label = ttk.Label(self.request_response_frame, text="", font=("Arial", 12))
        self.response_label.pack(pady=10)

    def send_request(self):
        request = self.request_input.get()
        if request:
            self.response_label.config(text="Sending request to server...")
            # Simulate server response delay using threading
            Thread(target=self.process_server_request, args=(request,)).start()

    def process_server_request(self, request):
        time.sleep(2)  # Simulate server processing time
        response = f"Server Response: Data for {request}"
        self.response_label.config(text=response)

    def setup_publish_subscribe(self):
        # Title
        ttk.Label(self.publish_subscribe_frame, text="Publish-Subscribe Simulation", font=("Arial", 14)).pack(pady=10)

        # Topik Entry for Publisher
        ttk.Label(self.publish_subscribe_frame, text="Publisher - Select Topic:").pack(pady=5)
        self.topic_choice_pub = ttk.Combobox(self.publish_subscribe_frame, values=["Peringatan Cuaca", "Peringatan Gempa"], state="readonly")
        self.topic_choice_pub.pack(pady=5)
        self.topic_choice_pub.set("Pilih Topik")

        # Message Entry for Publisher
        ttk.Label(self.publish_subscribe_frame, text="Publisher - Enter Message:").pack(pady=5)
        self.message_entry = ttk.Entry(self.publish_subscribe_frame, width=30)
        self.message_entry.pack(pady=5)

        # Button to publish message
        publish_button = ttk.Button(self.publish_subscribe_frame, text="Publish Message", command=self.publish_message)
        publish_button.pack(pady=10)

        # Listbox for subscribers
        ttk.Label(self.publish_subscribe_frame, text="Subscribers").pack(pady=5)
        self.subscriber_listbox = tk.Listbox(self.publish_subscribe_frame, height=5, width=80)
        self.subscriber_listbox.pack(pady=5)

        # Subscriber's Topic Selection
        ttk.Label(self.publish_subscribe_frame, text="Subscriber - Enter Name and Select Topic:").pack(pady=5)
        self.subscriber_name_entry = ttk.Entry(self.publish_subscribe_frame, width=30)
        self.subscriber_name_entry.pack(pady=5)
        
        self.topics = ["Peringatan Cuaca", "Peringatan Gempa"]
        self.topic_choice_sub = ttk.Combobox(self.publish_subscribe_frame, values=self.topics, state="readonly")
        self.topic_choice_sub.pack(pady=5)
        self.topic_choice_sub.set("Pilih Topik")
        
        # Button to subscribe to a topic
        subscribe_button = ttk.Button(self.publish_subscribe_frame, text="Subscribe to Topic", command=self.subscribe_to_topic)
        subscribe_button.pack(pady=10)

        # List of subscribers and their topics
        self.subscribers = {}

    def subscribe_to_topic(self):
        subscriber_name = self.subscriber_name_entry.get()
        selected_topic = self.topic_choice_sub.get()
        
        if subscriber_name and selected_topic != "Pilih Topik":
            # Update or add subscriber
            self.subscribers[subscriber_name] = selected_topic
            
            # Clear the listbox and repopulate it
            self.subscriber_listbox.delete(0, tk.END)  # Clear existing entries
            for sub, topic in self.subscribers.items():
                self.subscriber_listbox.insert(tk.END, f"{sub} -> {topic}")
        else:
            messagebox.showwarning("Error", "Please enter a valid subscriber name and select a topic.")

    def publish_message(self):
        topic = self.topic_choice_pub.get()
        message = self.message_entry.get()
        if topic and message:
            # Notify all subscribers of the selected topic
            if len(self.subscribers) == 0:
                messagebox.showwarning("No Subscribers", "There are no subscribers to receive the message.")
            else:
                for subscriber, subscribed_topic in self.subscribers.items():
                    if subscribed_topic == topic:
                        messagebox.showinfo("Notification", f"{subscriber} received -> Topic: {topic}, Message: {message}")
        else:
            messagebox.showwarning("Error", "Please select a topic and enter a message.")

# Initialize the Tkinter application
root = tk.Tk()
app = CommunicationSimulator(root)
root.mainloop()
