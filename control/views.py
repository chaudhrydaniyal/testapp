from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import SAFE_METHODS
from django.shortcuts import get_object_or_404


from rest_framework import (
    viewsets,
    generics,
    status,
    permissions,
    filters)

from .models import (
    Passage,
    Accessability,
    Document,
    Source,
    Topic,
    SharedLink,

)
from .serializers import (
    PassagesInfoSerializer,
    PassagesSerializer,
    AccessabilitySerializer,
    AccessabilityInfoSerializer,
    DocumentSerializer,
    DocumentInfoSerializer,
    SourceSerializer,
    SourceInfoSerializer,
    TopicSerializer,
    AccessabilitieDeleteSerializer,
    TopicInfoSerializer,
)


class PassagesViewSet(viewsets.ModelViewSet):
    queryset = Passage.objects.all().order_by("order")
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter]
    serializer_class = PassagesSerializer
    filterset_fields = ["id",
                        "document",
                        "header",
                        "header_level",
                        "anchor_text",
                        "anchor_url",
                        "order",
                        "is_active",
                        "created_at",
                        "updated_at",
                        ]
    search_fields = ["id",
                     "document",
                     "header",
                     "header_level",
                     "anchor_text",
                     "anchor_url",
                     "order",
                     "is_active",
                     "created_at",
                     "updated_at",
                     ]
    # http_method_names = ["PUT", "DELETE", "PATCH", "GET"]

    def get_serializer_class(self):
        if self.request is None:
            return PassagesSerializer
        elif not self.request.method in SAFE_METHODS:
            return PassagesSerializer
        return PassagesInfoSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['patch'])
    def bulk_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        queryset = self.filter_queryset(self.get_queryset())

        if isinstance(request.data, list):
            serializer = self.get_serializer(
                queryset, data=request.data, many=True, partial=partial)
        else:
            serializer = self.get_serializer(
                queryset, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(serializer.instance, '_prefetched_objects_cache', None):
            serializer.instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all().order_by("created_at")
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter]
    serializer_class = TopicSerializer
    filterset_fields = ["id",
                        "source",
                        "name",
                        "is_active",
                        "created_at",
                        "updated_at",
                        ]
    search_fields = ["id",
                     "source",
                     "name",
                     "is_active",
                     "created_at",
                     "updated_at",
                     ]

    def get_queryset(self):
        queryset = super().get_queryset()
        source_id = self.request.query_params.get('source')
        if source_id:
            queryset = queryset.filter(source_id=source_id)
        return queryset

    def get_serializer_class(self):
        if self.request is None:
            return TopicSerializer
        elif not self.request.method in SAFE_METHODS:
            return TopicSerializer
        return TopicInfoSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['patch'])
    def bulk_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        queryset = self.filter_queryset(self.get_queryset())

        if isinstance(request.data, list):
            serializer = self.get_serializer(
                queryset, data=request.data, many=True, partial=partial)
        else:
            serializer = self.get_serializer(
                queryset, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(serializer.instance, '_prefetched_objects_cache', None):
            serializer.instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all().order_by("created_at")
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter]
    serializer_class = SourceSerializer
    filterset_fields = ["id",
                        "name",
                        "user",
                        "detail_mode",
                        "is_active",
                        "created_at",
                        "updated_at",
                        ]
    search_fields = ["id",
                     "name",
                     "user",
                     "detail_mode",
                     "is_active",
                     "created_at",
                     "updated_at",
                     ]

    def get_serializer_class(self):
        if self.request is None:
            return SourceSerializer
        elif not self.request.method in SAFE_METHODS:
            return SourceSerializer
        return SourceInfoSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['patch'])
    def bulk_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        queryset = self.filter_queryset(self.get_queryset())

        if isinstance(request.data, list):
            serializer = self.get_serializer(
                queryset, data=request.data, many=True, partial=partial)
        else:
            serializer = self.get_serializer(
                queryset, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(serializer.instance, '_prefetched_objects_cache', None):
            serializer.instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by("order")
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter]
    serializer_class = DocumentSerializer

    filterset_fields = ["id", "topic", "raw_title", "title", "image_url", "image_alt",
                        "meta_description", "url", "author", "order", "is_active", "created_at", "updated_at"]
    search_fields = ["id", "topic", "raw_title", "title", "image_url", "image_alt",
                     "meta_description", "url", "author", "order", "is_active", "created_at", "updated_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        topic_id = self.request.query_params.get('topic')
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)
        return queryset

    def get_serializer_class(self):
        if self.request is None:
            return DocumentSerializer
        elif not self.request.method in SAFE_METHODS:
            return DocumentSerializer
        return DocumentInfoSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['patch'])
    def bulk_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        queryset = self.filter_queryset(self.get_queryset())

        if isinstance(request.data, list):
            serializer = self.get_serializer(
                queryset, data=request.data, many=True, partial=partial)
        else:
            serializer = self.get_serializer(
                queryset, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(serializer.instance, '_prefetched_objects_cache', None):
            serializer.instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class AccessabilityViewSet(viewsets.ModelViewSet):
    queryset = Accessability.objects.all().order_by("created_at")
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter]
    serializer_class = AccessabilitySerializer

    filterset_fields = ["id",
                        "document",
                        "term",
                        "position",
                        "volume",
                        "traffic",
                        "order",
                        "is_active",
                        "created_at",
                        "updated_at",
                        ]
    search_fields = ["id",
                     "document",
                     "term",
                     "position",
                     "volume",
                     "traffic",
                     "order",
                     "is_active",
                     "created_at",
                     "updated_at",
                     ]

    def get_serializer_class(self):
        if self.request is None:
            return AccessabilitySerializer
        elif not self.request.method in SAFE_METHODS:
            return AccessabilitySerializer
        return AccessabilityInfoSerializer

# @csrf_exempt
# def delete_accessability(request):
#     print(f"ENTERING ================> {request.POST}")
#     document_id = request.POST.get("document_id")
#     order = request.POST.get("order")
#     print(document_id)
#     print(order)
#     if request.method == "POST":
#         try:
#            document = Document.objects.get(id = str(request.POST.get("document_id")))
#         except Document.DoesNotExist:
#             return JsonResponse({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return JsonResponse({"error": e}, status=status.HTTP_400_BAD_REQUEST)

#         accessabilities = document.accessabilities_set.filter(order=request.POST.get('order'))
#         if accessabilities:
#             accessabilities.delete()
#             return JsonResponse({"message": "Accessability deleted successfully"}, status=status.HTTP_200_OK)
#         return JsonResponse({"message": "no accessabilities attached"}, status=status.HTTP_400_BAD_REQUEST)

#     return JsonResponse({"error": "Invalid request method."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class AccessabilitiesViewSet(viewsets.ModelViewSet):
    queryset = Accessability.objects.all().order_by("created_at")
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter]
    serializer_class = AccessabilitySerializer
    http_method_names = ["post",]
    filterset_fields = ["id",
                        "document",
                        "term",
                        "position",
                        "volume",
                        "traffic",
                        "order",
                        "is_active",
                        "created_at",
                        "updated_at",
                        ]
    search_fields = ["id",
                     "document",
                     "term",
                     "position",
                     "volume",
                     "traffic",
                     "order",
                     "is_active",
                     "created_at",
                     "updated_at",
                     ]

    def get_serializer_class(self):
        if self.request is None:
            return AccessabilitieDeleteSerializer
        elif not self.request.method in SAFE_METHODS:
            return AccessabilitieDeleteSerializer
        return AccessabilitieDeleteSerializer
