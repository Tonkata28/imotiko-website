from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from .models import Property, PropertyImage, PropertyInquiry, Favorite
from .serializers import (
    PropertySerializer, 
    PropertyListSerializer, 
    PropertyInquirySerializer,
    FavoriteSerializer
)

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.filter(is_available=True).order_by('-created_at')
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['property_type', 'transaction_type', 'city', 'bedrooms', 'bathrooms']
    search_fields = ['title', 'description', 'address', 'city']
    ordering_fields = ['price', 'area', 'created_at', 'views_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return PropertyListSerializer
        return PropertySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Price range filtering
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        # Bedroom filtering
        min_bedrooms = self.request.query_params.get('min_bedrooms')
        if min_bedrooms:
            queryset = queryset.filter(bedrooms__gte=min_bedrooms)
            
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment views count
        instance.views_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_properties = self.get_queryset().filter(is_featured=True)[:6]
        serializer = PropertyListSerializer(featured_properties, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        property_obj = self.get_object()
        property_obj.views_count += 1
        property_obj.save()
        return Response({'views_count': property_obj.views_count})

class FeaturedPropertiesView(APIView):
    def get(self, request):
        featured_properties = Property.objects.filter(
            is_featured=True, 
            is_available=True
        ).order_by('-created_at')[:6]
        
        serializer = PropertyListSerializer(
            featured_properties, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)

class PropertyStatsView(APIView):
    def get(self, request):
        stats = {
            'total_properties': Property.objects.filter(is_available=True).count(),
            'for_sale': Property.objects.filter(transaction_type='sale', is_available=True).count(),
            'for_rent': Property.objects.filter(transaction_type='rent', is_available=True).count(),
            'featured_count': Property.objects.filter(is_featured=True, is_available=True).count(),
            'avg_price_sale': Property.objects.filter(
                transaction_type='sale', 
                is_available=True
            ).aggregate(avg_price=Avg('price'))['avg_price'] or 0,
            'avg_price_rent': Property.objects.filter(
                transaction_type='rent', 
                is_available=True
            ).aggregate(avg_price=Avg('price'))['avg_price'] or 0,
            'cities': list(Property.objects.filter(is_available=True).values_list('city', flat=True).distinct()),
        }
        
        return Response(stats)

class PropertyInquiryCreateView(APIView):
    def post(self, request):
        serializer = PropertyInquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Inquiry sent successfully!'}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoriteToggleView(APIView):
    def post(self, request):
        property_id = request.data.get('property_id')
        session_key = request.session.session_key
        
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        try:
            property_obj = Property.objects.get(id=property_id)
            favorite, created = Favorite.objects.get_or_create(
                user_session=session_key,
                property=property_obj
            )
            
            if not created:
                favorite.delete()
                return Response({'favorited': False})
            
            return Response({'favorited': True})
            
        except Property.DoesNotExist:
            return Response(
                {'error': 'Property not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class FavoriteListView(APIView):
    def get(self, request):
        session_key = request.session.session_key
        
        if not session_key:
            return Response([])
            
        favorites = Favorite.objects.filter(user_session=session_key)
        serializer = FavoriteSerializer(favorites, many=True, context={'request': request})
        return Response(serializer.data)