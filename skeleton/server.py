import http.server
import socketserver
from audio import Audio
from motor import Motor
from jaw import Jaw
from time import sleep

PORT = 8000

audio = Audio()
motor = Motor()
jaw = Jaw()

distance = 60
armsRaised = False

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def playSound(self):
        audio.play('growl.mp3')
        jaw.open()
        sleep(2)
        jaw.close()

    def raiseArms(self):
        global armsRaised
        if not armsRaised:
            motor.driveDistance(1, distance)
            armsRaised = True

    def lowerArms(self):
        global armsRaised
        if armsRaised:
            motor.driveDistance(0, distance)
            armsRaised = False

    def do_GET(self):
        #print("A custom GET request was received.")
        # Call the parent class's do_GET method to serve the file
        super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])

        post_data = self.rfile.read(content_length)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        response_message = b"POST request received successfully!"
        self.wfile.write(response_message)

        #print(f"Received POST data: {post_data.decode('utf-8')}")

        data = post_data.decode('utf-8')
        print(f"Command received: {data}")
        if data == 'play':
            self.playSound()
        if data == 'up':
            self.raiseArms()
        if data == 'down':
            self.lowerArms()
        if data == 'reset':
            global armsRaised
            armsRaised = False

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at port {PORT} with a custom handler")
    httpd.serve_forever()
