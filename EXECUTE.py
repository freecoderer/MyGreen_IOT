# main_script.py

import subprocess

def main():
    # Start file1.py in a separate process
    process1 = subprocess.Popen(['python', 'face.py'])
    # Start file2.py in a separate process
    process2 = subprocess.Popen(['python', 'final_main.py'])
    # Wait for both processes to finish
    process1.wait()
    process2.wait()

if __name__ == '__main__':
    main()