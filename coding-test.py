# SPIDA job viewer and applier
# Benjamin Ryker

import json, requests

def displayJob(job):
    print(job["position"])
    print("\t" + job["description"])
    print("\tRequirements:")
    for req in job["requirements"]:
        print("\t\t" + req)

def viewApplication(appId):
    response = requests.get("https://dev.spidasoftware.com/apply/applications/%s" % appId)
    if response.text == "":
        print("No application found with that id")
        return
    app = json.loads(response.text)

    displayApplication(app)

    print()
    print("1: Delete")
    print("2: Return to main menu")
    selection = ""
    while selection not in ["1", "2"]:
        selection = input("What would you like to do? ")

    if selection == "1":
        deleteApplication(appId)
    elif selection == "2":
        return


def displayApplication(application):
    response = requests.get("https://dev.spidasoftware.com/apply/jobs/%s" % application["jobId"])
    job = json.loads(response.text)
    print("Application ID:", application["_id"])
    print("Job Title:", job["position"])
    print("Name:", application["name"])
    print("Justification:", application["justification"])
    print("Code:", application["code"])
    if "additionalLinks" in application:
        print("Additonal Links:")
        for link in application["additionalLinks"]:
            print("\t%s" % link)
    
def createApplication(jobId):
    print("Please enter the following fields to create your application:")
    print()

    application = {}
    application["name"] = input("First and last name: ")
    application["jobId"] = jobId
    application["justification"] = input("Why we should hire you: ")
    application["code"] = input("Link to the source code for your submission: ")

    application["additionalLinks"] = []
    newLink = None
    print("Additional Links (github, Google code, etc): ")
    print("Leave blank to stop adding more links")
    while newLink != "":
        newLink = input("Link: ")
        if newLink != "":
            application["additionalLinks"].append(newLink)
    
    return application

def deleteApplication(appId):
    requests.delete("https://dev.spidasoftware.com/apply/applications/%s" % appId)

def viewJobs():
    print("Loading jobs...")

    response = requests.get("https://dev.spidasoftware.com/apply/jobs")
    joblist = json.loads(response.text)

    for i in range(len(joblist)):
        print("%d: " % i, end = "")
        displayJob(joblist[i])
    
    selection = input("Which job would you like to apply for? ")
    job = None
    while job == None:
        try:
            job = joblist[int(selection)]
        except:
            if selection == "exit":
                return
            else:
                selection = input("Invalid selection, please choose a job or type 'exit' to exit: ")

    print()
    print("You have selected job: %s" % job["position"])

    application = createApplication(job["_id"])

    response = requests.post("https://dev.spidasoftware.com/apply/applications", json=application)
    submission = json.loads(response.text)
    
    print("You have successfully submitted your application")
    print()
    displayApplication(submission)

if __name__ == "__main__":
    print("Welcome to SPIDA's Job Site")
    while True:
        print()
        print("Main Menu")
        print("1: View and apply to jobs")
        print("2: View or delete application")
        print("3: Exit")

        selection = ""
        while selection not in ["1", "2", "3"]:
            selection = input("What would you like to do? ")

        if selection == "1":
            viewJobs()
        elif selection == "2":
            appId = input("Enter the application id: ")
            while len(appId) != 24:
                print("Invalid id")
                appId = input("Enter the application id: ")
            viewApplication(appId)
        elif selection == "3":
            exit(0)
        
