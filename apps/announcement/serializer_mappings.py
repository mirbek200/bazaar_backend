# serializer_mappings.py

from apps.announcement.serializers import (
    CarsSerializer, MotorcyclesSerializer,
    MopedsSerializer, TransfersSerializer, TakeOffSerializer, BuySerializer,
    ServicesCargoTransportationSerializer, ClothSerializer, ShoesSerializer,
    AccessoriesSerializer, BeautyHealthSerializer, ProductsForChildrenSerializer,
    ElectronicsSerializer, LookingEmployeeSerializer, LookingJobSerializer,
    CarsListDetailSerializer, MotorcyclesListDetailSerializer, MopedsListDetailSerializer,
    TransfersListDetailSerializer, TakeOffListDetailSerializer, BuyListDetailSerializer,
    ServicesCargoTransportationListDetailSerializer, ClothListDetailSerializer, ShoesListDetailSerializer,
    AccessoriesListDetailSerializer, BeautyHealthListDetailSerializer, ProductsForChildrenListDetailSerializer,
    ElectronicsListDetailSerializer, LookingEmployeeListDetailSerializer, LookingJobListDetailSerializer,
)

from apps.announcement.models import (
    Cars, Motorcycles, Mopeds, Transfers,
    TakeOff, Buy, ServicesCargoTransportation, Cloth,
    Shoes, Accessories, BeautyHealth, ProductsForChildren,
    Electronics, LookingEmployee, LookingJob,
)

serializer_classes = {
    'transport': {
        'car': CarsSerializer,
        'motorcycle': MotorcyclesSerializer,
        'moped': MopedsSerializer,
        'transfer': TransfersSerializer,
    },
    'real_estates': {
        'takeoff': TakeOffSerializer,
        'buy': BuySerializer,
    },
    'services': {
        'cargo_transportation': ServicesCargoTransportationSerializer,
    },
    'personal_items': {
        'cloth': ClothSerializer,
        'shoes': ShoesSerializer,
        'accessories': AccessoriesSerializer,
        'beauty_health': BeautyHealthSerializer,
        'products_for_children': ProductsForChildrenSerializer,
    },
    'electronics': {
        'electronics': ElectronicsSerializer,
    },
    'jobs': {
        'looking_employee': LookingEmployeeSerializer,
        'looking_job': LookingJobSerializer,
    },
}

model_mapping = {
    'transport': {
        'car': Cars,
        'motorcycle': Motorcycles,
        'moped': Mopeds,
        'transfer': Transfers,
    },
    'real_estates': {
        'takeoff': TakeOff,
        'buy': Buy,
    },
    'services': {
        'cargo_transportation': ServicesCargoTransportation,
    },
    'personal_items': {
        'cloth': Cloth,
        'shoes': Shoes,
        'accessories': Accessories,
        'beauty_health': BeautyHealth,
        'products_for_children': ProductsForChildren,
    },
    'electronics': {
        'electronics': Electronics,
    },
    'jobs': {
        'looking_employee': LookingEmployee,
        'looking_job': LookingJob,
    },
}

serializer_list_detail_classes = {
    'transport': {
        'car': CarsListDetailSerializer,
        'motorcycle': MotorcyclesListDetailSerializer,
        'moped': MopedsListDetailSerializer,
        'transfer': TransfersListDetailSerializer,
    },
    'real_estates': {
        'takeoff': TakeOffListDetailSerializer,
        'buy': BuyListDetailSerializer,
    },
    'services': {
        'cargo_transportation': ServicesCargoTransportationListDetailSerializer,
    },
    'personal_items': {
        'cloth': ClothListDetailSerializer,
        'shoes': ShoesListDetailSerializer,
        'accessories': AccessoriesListDetailSerializer,
        'beauty_health': BeautyHealthListDetailSerializer,
        'products_for_children': ProductsForChildrenListDetailSerializer,
    },
    'electronics': {
        'electronics': ElectronicsListDetailSerializer,
    },
    'jobs': {
        'looking_employee': LookingEmployeeListDetailSerializer,
        'looking_job': LookingJobListDetailSerializer,
    },
}
