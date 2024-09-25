from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from logging_config import configure_logging
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from django.shortcuts import get_object_or_404


# Configure logging
logger = configure_logging()


# Product CRUD Operations
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list(request):
    try:
        if request.method == 'GET':

            cached_products = cache.get('products_list')
            if cached_products:
                logger.info("Fetching products from cache")
                return Response(cached_products)

            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            logger.info("Fetching products from database")
            cache.set('products_list', serializer.data, timeout=60 * 15)  # Cache for 15 minutes
            return Response(serializer.data)

        # elif request.method == 'POST':
        #     serializer = ProductSerializer(data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.info("Error :" + str(e))
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Product CRUD Operations
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_add(request):
    try:
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            category_id = request.data.get('category')
            product_name = request.data.get('product_name')
            prod = Product.objects.filter(category_id=category_id, product_name=product_name).first()
            if not prod:
                product = serializer.save(user=request.user)
                cache.delete('products_list')
                logger.info("Added products from database")
                response_serializer = ProductSerializer(product)

                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

            else:
                logger.info("Product already exists.")
                return Response({'error': 'Product already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        logger.error(f"Not able to add data")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_detail(request, product_id):
    try:
        cache_name = 'products_list_' + str(product_id)
        product = get_object_or_404(Product, pk=product_id)

        if request.method == 'GET':
            cached_item = cache.get(cache_name)
            if cached_item:
                logger.info(f"Fetching products from cache {product_id}")
                return Response(cached_item)

            serializer = ProductSerializer(product)

            logger.info("Fetching products from database")
            cache.set(cache_name, serializer.data, timeout=60 * 15)  # Cache for 15 minutes

            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                cache.delete(cache_name)
                cache.delete('product_list')
                logger.info("Updating products from database")
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            prod = product.delete()
            cache.delete(cache_name)
            cache.delete('product_list')
            logger.info("Deleting products from database")
            return Response({'result': 'Product deleted successfully.'}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)