from .models import Source, User
from rest_framework import serializers
from .models import Accessability, Document, Passage, Source, Topic
from .models import User


class AccessabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Accessability
        fields = "__all__"


class AccessabilityInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessability
        depth = 1
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):
    csv_file = serializers.FileField(
        required=False, allow_null=True, write_only=True)
    accessability_one = serializers.SerializerMethodField(read_only=True)
    accessability_two = serializers.SerializerMethodField(read_only=True)
    accessability_three = serializers.SerializerMethodField(read_only=True)
    accessibility_position = serializers.CharField(
        write_only=True, required=False, allow_null=True)

    class Meta:
        model = Document
        # fields = ("accessability_1", "csv_file")
        extra_kwargs = {'csv_file': {'write_only': True,
                                     'required': False, "allow_blank": True}}
        fields = ("topic",
                  "raw_title",
                  "title",
                  "image_url",
                  "image_alt",
                  "meta_description",
                  "url",
                  "author",
                  "csv_file",
                  "order",
                  "url",
                  "id",
                  "is_active",
                  "created_at",
                  "updated_at",
                  "accessibility_position",
                  "accessability_one",
                  "accessability_two",
                  "accessability_three", )

    def get_accessability_one(self, obj):
        # Example logic assuming AccessabilityInfoSerializer is correctly defined
        return AccessabilitySerializer(obj.accessability_set.filter(order=1), many=True).data

    def get_accessability_two(self, obj):
        # Example logic assuming AccessabilityInfoSerializer is correctly defined
        return AccessabilitySerializer(obj.accessability_set.filter(order=2), many=True).data

    def get_accessability_three(self, obj):
        # Example logic assuming AccessabilityInfoSerializer is correctly defined
        return AccessabilitySerializer(obj.accessability_set.filter(order=3), many=True).data

    def add_accessibility(self, csv_file, document, access_position):
        import pandas as pd

        dt = pd.read_csv(csv_file)
        columns = dt.columns.tolist()
        dt["Current position"].fillna(0, inplace=True)
        for index, row in dt.iterrows():
            # print(row["Current position"])
            try:
                Accessability.objects.create(
                    term=row["Keyword"],
                    volume=row["Volume"],
                    document=document,
                    position=row["Current position"] if row["Current position"] is not pd.NA else 0,
                    order=access_position
                )
            except Exception as e:
                raise ValueError({"error": str(e)})

    def create(self, validated_data):
        csv_file = validated_data.pop("csv_file", None)
        # Handle the creation logic here
        document = Document.objects.create(**validated_data)
        passage = Passage.objects.create(header_level="H1", document=document)
        if csv_file:
            self.add_accessibility(csv_file, document)
        return document

    def update(self, instance, validated_data):

        csv_file = validated_data.pop("csv_file", None)
        access_position = validated_data.pop("accessibility_position", None)

        if csv_file:
            self.add_accessibility(csv_file, instance, access_position)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class DocumentInfoSerializer(serializers.ModelSerializer):
    accessability_one = serializers.SerializerMethodField(read_only=True)
    accessability_two = serializers.SerializerMethodField(read_only=True)
    accessability_three = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Document
        depth = 1
        fields = ("topic",
                  "raw_title",
                  "title",
                  "image_url",
                  "image_alt",
                  "meta_description",
                  "url",
                  "author",
                  "order",
                  "url",
                  "id",
                  "is_active",
                  "created_at",
                  "updated_at",
                  "accessability_one",
                  "accessability_two",
                  "accessability_three", )

    def get_accessability_one(self, obj):
        # Example logic assuming AccessabilityInfoSerializer is correctly defined
        return AccessabilitySerializer(obj.accessability_set.filter(order=1), many=True).data

    def get_accessability_two(self, obj):
        # Example logic assuming AccessabilityInfoSerializer is correctly defined
        return AccessabilitySerializer(obj.accessability_set.filter(order=2), many=True).data

    def get_accessability_three(self, obj):
        # Example logic assuming AccessabilityInfoSerializer is correctly defined
        return AccessabilitySerializer(obj.accessability_set.filter(order=3), many=True).data


class SourceSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False, allow_null=True)
    document_count = serializers.SerializerMethodField(read_only=True)
    topics = serializers.SerializerMethodField(read_only=True)

    def get_topics(self, obj):
        return TopicSerializer(obj.topics.all(), many=True).data

    def get_document_count(self, obj):
        count = 0
        for topic in obj.topics.all():
            count += topic.documents.count()
            return count

    class Meta:
        model = Source
        fields = ["id", "user", "name", "topics", "detail_mode",
                  "created_at", "updated_at", "document_count"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user

        # Handle the creation logic here
        source = Source.objects.create(**validated_data)
        return source


class SourceInfoSerializer(serializers.ModelSerializer):
    document_count = serializers.SerializerMethodField(read_only=True)
    topics = serializers.SerializerMethodField(read_only=True)

    def get_topics(self, obj):
        return TopicSerializer(obj.topics.all(), many=True).data

    def get_document_count(self, obj):
        count = 0
        for topic in obj.topics.all():
            count += topic.documents.count()
            return count

    class Meta:
        model = Source
        depth = 1
        fields = ["id", "user", "name", "topics", "detail_mode",
                  "created_at", "updated_at", "document_count"]


class TopicSerializer(serializers.ModelSerializer):
    passages = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()

    def get_passages(self, obj):
        count = 0
        for document in obj.documents.all():
            count += document.passage_set.count()
            return count
        return count

    def get_documents(self, obj):
        return DocumentSerializer(obj.documents.all(), many=True).data

    class Meta:
        model = Topic
        fields = ["id", "name", "source", "documents",
                  "passages", "is_active", "created_at", "updated_at"]
        extra_kwargs = {'documents': {'read_only': True},
                        'passages': {'read_only': True}}

    # def get_document(self, obj):
    #     return obj.documents.all()


class TopicInfoSerializer(serializers.ModelSerializer):
    passages = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()

    def get_passages(self, obj):
        count = 0
        for document in obj.documents.all():
            count += document.passage_set.count()
            return count

    def get_documents(self, obj):
        return DocumentSerializer(obj.documents.all(), many=True).data

    class Meta:
        model = Topic
        depth = 1
        fields = ["id", "name", "source", "documents",
                  "passages", "is_active", "created_at", "updated_at"]
        extra_kwargs = {'documents': {'read_only': True},
                        'passages': {'read_only': True}}

    # def get_document(self, obj):
    #     return obj.documents.all()


class PassagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passage
        fields = "__all__"

        # read_only_fields = ('accessability', )  # Add any other read-only fields you need


class PassagesInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passage
        depth = 1
        fields = "__all__"


class AccessabilitieDeleteSerializer(serializers.ModelSerializer):
    document_id = serializers.CharField(
        write_only=True, required=False, allow_null=True)
    order = serializers.CharField(
        write_only=True, required=False, allow_null=True)

    class Meta:
        model = Document
        depth = 1
        fields = ("document_id", "order")

    def create(self, validated_data):
        document_id = validated_data.get("document_id")
        order = validated_data.get("order")
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            raise ValueError({"error": "Document does not exists"})
        except Exception as e:
            # return JsonResponse({"error": e}, status=status.HTTP_400_BAD_REQUEST)
            raise ValueError({"error": e})

        accessabilities = document.accessability_set.filter(order=order)
        if accessabilities:
            accessabilities.delete()
        return document
