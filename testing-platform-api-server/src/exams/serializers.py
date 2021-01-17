from rest_framework import serializers
from django.core.files import File

from src.exams.models import Choice, Question, Exam, ExamResult, Domain, Subject, Problem,\
    ProblemAttachment, ActualProblemAttachment, DiffProblemAttachment, GraphEditDistance
from src.users.serializers import UserSerializer


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        exclude = ()


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'question']  # don't serialize correct_answer, so that no cheating can occur
        depth = 1


class CreateChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        exclude = ()
        depth = 1


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'exam', 'choices', 'num_correct_answers']
        depth = 1


class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    subject = SubjectSerializer(many=False)
    creator = UserSerializer(many=False)

    class Meta:
        model = Exam
        exclude = ('completed_by',)
        depth = 2


class ExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = ['id', 'score', 'response_pattern', 'state']


class CreateExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = ['exam', 'score', 'choices', 'user', 'response_pattern', 'state']


class CreateQuestionSerializer(serializers.ModelSerializer):
    choices = CreateChoiceSerializer(many=True)

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        question = Question.objects.create(**validated_data)
        for choice in choices:
            serializer = CreateChoiceSerializer(data=choice)
            serializer.is_valid(raise_exception=True)
            ret_val = serializer.save()
            question.choices.add(ret_val)

        return question

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'exam', 'choices']
        depth = 1


class ProblemAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemAttachment
        exclude = ()


class ActualProblemAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActualProblemAttachment
        exclude = ()


class DiffProblemAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiffProblemAttachment
        exclude = ()


class ProblemSerializer(serializers.ModelSerializer):
    """ read_only=True because create() doesn't support writable nested fields by default
    (used in ProblemViewSet -> custom_make)"""
    source_problems = ProblemAttachmentSerializer(many=True, read_only=True)
    target_problems = ProblemAttachmentSerializer(many=True, read_only=True)

    actual_source_problems = ActualProblemAttachmentSerializer(many=True, read_only=True)
    actual_target_problems = ActualProblemAttachmentSerializer(many=True, read_only=True)

    diff_source_problems = DiffProblemAttachmentSerializer(many=True, read_only=True)
    diff_target_problems = DiffProblemAttachmentSerializer(many=True, read_only=True)

    question_text = serializers.CharField(write_only=True)
    choices = serializers.ListField(write_only=True)
    exam = serializers.IntegerField(write_only=True)

    class Meta:
        model = Problem
        exclude = ()

    def create(self, validated_data):
        question_text = validated_data.pop('question_text')
        choices = validated_data.pop('choices')
        exam_id = validated_data.pop('exam')

        exam = Exam.objects.get(pk=exam_id)

        question = Question.objects.create(question_text=question_text, exam=exam)
        for choice in choices:
            serializer = CreateChoiceSerializer(data=choice)
            serializer.is_valid(raise_exception=True)
            ret_val = serializer.save()
            question.choices.add(ret_val)

        problem = Problem.objects.create(question=question, **validated_data)

        return problem

class CreateExamSerializer(serializers.ModelSerializer):
    questions = CreateQuestionSerializer(many=True)

    def create(self, validated_data):
        questions = validated_data.pop('questions')
        exam = Exam.objects.create(**validated_data)
        for question in questions:
            serializer = CreateQuestionSerializer(data=question)
            serializer.is_valid(raise_exception=True)
            exam.questions.add(serializer.save())
        self.generate_ims_qti(exam)
        return exam

    def generate_ims_qti(self, exam):
        file = File(open(f'./static/{exam.id}.xml', 'a'))

        data = '<?xml version="1.0" encoding="UTF-8"?>\n<qti-assessment-items>'
        for q in exam.questions.all():
            data += '\n\t<qti-assessment-item\n\t \
    xmlns="http://www.imsglobal.org/xsd/qti/imsqtiasi_v3p0"\n\t \
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n\t \
    xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqtiasi_v3p0\n\t \
            https://purl.imsglobal.org/spec/qti/v3p0/schema/xsd/imsqti_asiv3p0_v1p0.xsd"\n\t \
    identifier="' + str(q.id) + '"\n\t \
    time-dependent="false"\n\t \
    xml:lang="en-US">\n\t\t'

            correct_answers = '''<qti-response-declaration base-type="identifier" cardinality="single" identifier="RESPONSE">
            <qti-correct-response>\n\t'''
            choices = []
            for choice in q.choices.all():
                choices.append(f'<qti-simple-choice identifier="{choice.id}">{choice.choice_text}</qti-simple-choice>\n\t\t\t')
                if choice.correct_answer:
                    correct_answers += '\t\t\t\t<qti-value>' + choice.choice_text + '</qti-value>\n\t\t\t\t'

            correct_answers += '\t\t</qti-correct-response>\n\t\t</qti-response-declaration>\n\t\t'

            data += correct_answers

            # how to score - award a single point for answering the question correctly
            data += '<qti-outcome-declaration base-type="float" cardinality="single" identifier="SCORE">\n\t \
        <qti-default-value>\n\t \
            <qti-value>1</qti-value>\n\t \
        </qti-default-value>\n\t \
    </qti-outcome-declaration>\n\t\t'

            data += '<qti-item-body>\n\t\t\t<p>'
            data += q.question_text + '</p>\n\t\t\t'
            data += '<qti-choice-interaction max-choices="1" min-choices="1" response-identifier="RESPONSE">\n\t\t\t\t'
            for i in range(len(choices)):
                data += choices[i]
                if i != len(choices) - 1:
                    data += '\t\t'

            data += '</qti-choice-interaction>\n\t\t</qti-item-body>\n\t\t'

            data += '<qti-response-processing \
template="https://purl.imsglobal.org/spec/qti/v3p0/rptemplates/match_correct"/>\n\t'
            data += '</qti-assessment-item>'
            file.write(data)
            data = ''
        file.write('\n</qti-assessment-items>')
        file.close()

    class Meta:
        model = Exam
        exclude = ()


class DomainSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(many=False)
    problems = ProblemSerializer(many=True)

    class Meta:
        model = Domain
        exclude = ()


class GraphEditDistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphEditDistance
        exclude = ('exam',)
