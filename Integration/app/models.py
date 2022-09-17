from django.db import models


class Participant(models.Model):
    Username = models.CharField(max_length=30)
    Score = models.IntegerField(default=0)
    First_Student_Name = models.CharField(max_length=50)
    Second_Student_Name = models.CharField(max_length=50)
    Number_Of_Tests = models.IntegerField(default=0)

    def __str__(self):
        return self.Username


class Advancement(models.Model):
    Problem_Id = models.IntegerField()
    Participant_Id = models.IntegerField()
    Wrote_Code = models.TextField(default="")
    Score = models.IntegerField(default=0)
    Percentage = models.IntegerField(default=0)
    Color = models.CharField(max_length=30, default="black")
    Results = models.CharField(max_length=500, default="")
    Number_Of_Tests = models.IntegerField(default=0)

    def __str__(self):
        return "Advancement of {} in {}".format(Participant.objects.get(id=self.Participant_Id),
                                                Problem.objects.get(id=self.Problem_Id))


class Problem(models.Model):
    Name = models.CharField(max_length=200)
    Image_Url = models.CharField(max_length=200)
    Statement_Url = models.CharField(max_length=200)
    Python_User_Code = models.TextField(default="#write your code here")
    Python_Server_Code = models.TextField(default="#write your code here")
    Score = models.IntegerField()
    Time_Limit_Per_Test = models.FloatField(default=1)

    def __str__(self):
        return self.Name


class Test(models.Model):
    Problem_Id = models.IntegerField()
    Test_Id = models.IntegerField()
    Input = models.TextField()
    Expected_Output = models.TextField()
    Score = models.IntegerField()

    def __str__(self):
        return "{}-{}".format(Problem.objects.get(id=self.Problem_Id), self.Test_Id)
