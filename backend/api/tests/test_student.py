from api.serializers import StudentSerializer
import json
from api.models import Student, AcademicPlan
from rest_framework import status
from rest_framework.test import APITestCase
from .test_setup_function import setup, login


class StudentTestCase(APITestCase):

    def setUp(self):
        login(self.client)
        setup(self)

    def test_post_student_data(self):
        student = [{"matricNo": "1234567", "givenNames": "Philip J", "surname": "Fry", "academicPlan": "F100-2208",
                    "finalAward1": 0.0}]
        response = self.client.post("/api/students/", student, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_data_stored(self):
        data = [{"matricNo": "1234567", "givenNames": "Philip J", "surname": "Fry", "academicPlan": "F100-2208",
                 "finalAward1": 0.0, "finalAward2": 0.00, "finalAward3": 0.000},
                {"matricNo": "7654321", "givenNames": "Hermes", "surname": "Conrad", "academicPlan": "F100-2208",
                 "finalAward1": 0.0, "finalAward2": 0.00, "finalAward3": 0.000}]
        serializer = StudentSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
        student1 = Student.objects.filter(matricNo="1234567", givenNames="Philip J", surname="Fry",
                                          academicPlan="F100-2208", finalAward1=0.0, finalAward2=0.00,
                                          finalAward3=0.000).exists()
        student2 = Student.objects.filter(matricNo="7654321", givenNames="Hermes", surname="Conrad",
                                          academicPlan="F100-2208", finalAward1=0.0, finalAward2=0.00,
                                          finalAward3=0.000).exists()
        self.assertTrue(student1)
        self.assertTrue(student2)

    def test_get_student_object(self):
        response = self.client.get('/api/students/')
        response = response.content.decode('utf-8')
        response_dict = json.loads(response)
        self.assertEqual(response_dict, [{"matricNo": "2894029", "givenNames": "Zak", "surname": "Bagans",
                                          "academicPlan": "F100-2208", "finalAward1": '0.0', "finalAward2": '0.00',
                                          "finalAward3": '0.000', "updatedAward": "-1"},
                                         {"matricNo": "2283853", "givenNames": "Robert", "surname": "Goulet",
                                          "academicPlan": "F100-2208", "finalAward1": '0.0', "finalAward2": '0.00',
                                          "finalAward3": '0.000', "updatedAward": "-1"}])

    def test_duplicate_student_entries_not_created(self):
        student = [{"matricNo": "2894029", "givenNames": "Zak", "surname": "Bagans",
                    "academicPlan": "F100-2208", "finalAward1": 0.0, "finalAward2": None, "finalAward3": None}]
        response = self.client.post("/api/students/", student, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_get_student_when_logged_out(self):
        self.client.logout()
        Student.objects.get_or_create(matricNo="1234567", givenNames="Lionel", surname="Hutz",
                                      academicPlan=AcademicPlan.objects.get(planCode="F100-2208"), finalAward1=0.0,
                                      finalAward2=None, finalAward3=None)
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_post_student_data_when_logged_out(self):
        self.client.logout()
        student = [{"matricNo": "1234567", "givenNames": "Philip J", "surname": "Fry", "academicPlan": "CHEM_1234",
                    "finalAward1": 0.0, "finalAward2": None, "finalAward3": None}]
        response = self.client.post("/api/students/", student, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        student_exists = Student.objects.filter(matricNo="1234567", givenNames="Phillip J", surname="Fry",
                                                academicPlan="CHEM_1234", finalAward1=0.0, finalAward2=None,
                                                finalAward3=None).exists()
        self.assertFalse(student_exists)

    def test_gpa_decimals(self):
        matric_no = "1234567"
        data = [{"matricNo": matric_no, "givenNames": "Philip J", "surname": "Fry",
                 "academicPlan": "F100-2208", "finalAward3": 1.200}]
        serializer = StudentSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()

        student = Student.objects.get(matricNo=matric_no)
        self.assertEqual(str(student.finalAward1), '1.2')
        self.assertEqual(str(student.finalAward2), '1.20')
        self.assertEqual(str(student.finalAward3), '1.200')

        student.finalAward1 = 1.23
        student.save()

        self.decimal_assertion()

        student.finalAward1 = 1.232
        student.save()

        self.decimal_assertion()

        final_award3_dec = str(student.finalAward3).partition('.')[-1]
        self.assertEqual(len(final_award3_dec), 3)

    def decimal_assertion(self):
        matric_no = "1234567"
        student = Student.objects.get(matricNo=matric_no)

        final_award1_dec = str(student.finalAward1).partition('.')[-1]
        self.assertEqual(len(final_award1_dec), 1)

        final_award2_dec = str(student.finalAward2).partition('.')[-1]
        self.assertEqual(len(final_award2_dec), 2)
