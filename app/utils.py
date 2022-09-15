from .models import *
import http.client
import json
import pandas as pd
import django.contrib.auth
from django.db.models import Q


def get_participant(request):
    current_user = request.user
    participant = Participant.objects.get(Username=current_user.username)
    return participant


def get_advancement(problem, participant):
    try:
        advancement = Advancement.objects.get(Problem_Id=problem.id, Participant_Id=participant.id)
    except:

        List = ["{},0,0%,black".format(i+1) for i in range(problem.Number_Of_Tests)]
        advancement = Advancement(Problem_Id=problem.id, Participant_Id=participant.id,
                                  Results=" ".join(List), Wrote_Code=problem.Python_User_Code)
        advancement.save()
    results = advancement.Results.split(" ")
    results = [ele.split(",") for ele in results]
    return advancement, results


def get_Input(id):
    tests = Test.objects.filter(Problem_Id=id, Type="submit").order_by('Test_Id')
    inputs = [test.Input.replace("\r", "") for test in tests]
    return "\n".join(inputs)


def get_outputs(code, Input):
    language = "python3"
    conn = http.client.HTTPSConnection("api.jdoodle.com")
    payload = json.dumps({
        "script": code,
        "language": language,
        "stdin": Input,
        "versionIndex": "0",
        "clientId": "b5b89aead5686391c071fdc29db5169",
        "clientSecret": "75bcee08f44431434b50aac5cfd69d8a00e83c2188ec29ae65eb688858ddc1b2"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1/execute", payload, headers)
    res = conn.getresponse()
    data = res.read()
    string_output = data.decode("utf-8")
    dictionary_output = json.loads(string_output)
    print(dictionary_output)
    results = dictionary_output['output'].rstrip("\n").split("\n")
    outputs = []
    for result in results:
        try:
            l = result.split("|")
            Tuple = (l[0], float(l[1]))
            outputs.append(Tuple)
        except:
            outputs = "error"
            break
    return outputs


def get_color(percentage):
    if percentage < 50:
        color = "red"
    elif percentage > 50 and percentage < 70:
        color = "orange"
    else:
        color = "green"
    return color


def get_response(request, user_code, id):
    results = []
    Total_Score = 0
    problem = Problem.objects.get(id=id)
    server_code = problem.Python_Server_Code
    code = "{}\n{}".format(user_code, server_code)
    Input = get_Input(id)
    outputs = get_outputs(code, Input)
    if outputs == "error":
        results = ["{},0,Error,red".format(i) for i in range(1, 11)]
    else:
        for index, output in enumerate(outputs):
            test = Test.objects.get(Problem_Id=problem.id, Test_Id=index+1, Type="submit")
            result_of_test, running_time = output
            if running_time <= problem.Time_Limit_Per_Test:
                if result_of_test == test.Expected_Output:
                    results.append("{},{},Passed,green".format(test.Test_Id, test.Score))
                    Total_Score += test.Score
                else:
                    results.append("{},{},WrongAnswer,red".format(test.Test_Id, test.Score))
            else:
                results.append("{},{},RunningTime,red".format(test.Test_Id, test.Score))
    print(Total_Score)
    Total_Score, percentage = get_score_percentage(Total_Score, request, id)
    color = get_color(percentage)
    information = [Total_Score, percentage, color, " ".join(results)]
    results.append("{},{},{}".format(Total_Score, percentage, color))
    response = " ".join(results)
    return response, information


def get_score_percentage(score, request, id):
    problem = Problem.objects.get(id=id)
    participant = get_participant(request)
    advancement = Advancement.objects.get(Problem_Id=id, Participant_Id=participant.id)
    NewScore = round(score-advancement.Number_Of_Tests * 0.01 * problem.Score, 2)
    percentage = round(100 * NewScore / problem.Score, 2)
    if NewScore >= 0 and percentage >= 0:
        return NewScore, percentage
    return 0, 0


def Update_Advancement(request, problem_id, code, information):
    problem = Problem.objects.get(id=problem_id)
    participant = get_participant(request)
    advancement = Advancement.objects.get(Problem_Id=problem.id, Participant_Id=participant.id)
    advancement.Wrote_Code = code
    advancement.Number_Of_Tests += 1
    advancement.Score = information[0]
    advancement.Percentage = information[1]
    advancement.Color = information[2]
    advancement.Results = information[3]
    advancement.save()


def Update_Score(request):
    participant = get_participant(request)
    advancements = Advancement.objects.filter(Participant_Id=participant.id)
    participant.Score = sum([advancement.Score for advancement in advancements])
    participant.Number_Of_Tests = sum([advancement.Number_Of_Tests for advancement in advancements])
    participant.save()


def fill_problem(path):
    Problem.objects.all().delete()
    problems = pd.read_excel(path)
    for i in range(problems.shape[0]):
        row = problems.iloc[i]
        problem = Problem(id=row["problem_id"],
                          Name=row["name"],
                          Image_Url=row["image_path"],
                          Statement_Url=row["statement_path"],
                          Score=row["score"],
                          Python_User_Code=row["python_user_code"],
                          Python_Server_Code=row["python_server_code"],
                          Number_Of_Tests=10,
                          Time_Limit_Per_Test=row["time_limit"])
        problem.save()


def fill_test(path):
    Test.objects.all().delete()
    tests = pd.read_excel(path)
    for i in range(tests.shape[0]):
        row = tests.iloc[i]
        test = Test(Problem_Id=row["problem_id"],
                    Test_Id=row["test_id"],
                    Input=row["input"],
                    Expected_Output=row["expected_output"],
                    Type="submit",
                    Score=row["score"])

        test.save()


def fill_participant_user(path):
    Participant.objects.filter(~Q(Username="e-plusplus")).delete()
    User = django.contrib.auth.get_user_model()
    User.objects.filter(is_superuser=False).delete()
    df = pd.read_excel(path)
    for i in range(df.shape[0]):
        row = df.iloc[i]
        participant = Participant(Username=row["username"], First_Student_Name=row["first student"], Second_Student_Name=row["second student"])
        participant.save()
        user = User.objects.create_user(row["username"], password=row["password"])
        user.is_superuser = False
        user.save()

def get_percentage_color(problem, participant):
    try:
        advancement = Advancement.objects.get(Problem_Id=problem.id, Participant_Id=participant.id)
        return advancement.Percentage, advancement.Color
    except:
        return 0, "black"
