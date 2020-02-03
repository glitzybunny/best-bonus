import datetime

from django.db import models
from django.db.models import Q, Max
from django.core.validators import MaxValueValidator

SUPLIER_TYPES = (
    (0, 'Casino'),
    (1, 'Betting'),
    (2, 'CS:GO'),

)

BONUS_TYPES = (
    (0, 'Deposit'),
    (1, 'Freespin'),

)

class Suplier(models.Model):
    '''
    Suplier/Casino entity sdescribes app/compnay/resource what distributes bonuses.
    e.g. Online casino, Betting company, Gambling app, etc
    '''

    title = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name="Name")
    image = models.ImageField(upload_to="casino_logos/", blank=True, null=True, verbose_name="Suplier image")
    ca_license_bool = models.BooleanField(default=False, verbose_name="License")
    suplier_type = models.IntegerField(choices=SUPLIER_TYPES, default=0)

    def __str__(self):
        return self.title


def today_plus_30_days():
    # Created for DOE field default in Bonus model 
    # It is here, because Django does not serialize lambda functions
    return datetime.date.today() + datetime.timedelta(days=30)

def get_parsed_json(unparsed_obj):
    """
    Takes JSON response array and returns a parsed dict for FilterMechanism 
    e.g
    Takes:
    .............parsingObject: UNPARSED(list)
    [{'name': 'sorting', 'value': 'dep_min_to_max'}, 
    {'name': 'type', 'value': 'all'}, 
    {'name': 'wager-js-range-slider', 'value': '0;42'}, 
    {'name': 'bonus-js-range-slider', 'value': '0;5000'}, 
    {'name': 'deposit-js-range-slider', 'value': '0;10000'}]

    Returns:
    .................parsingObject: PARSED(dict)
    {'sorting': 'dep_min_to_max', 'type': 'all', 'wager-js-range-slider': '0;42',
    'bonus-js-range-slider': '0;5000', 'deposit-js-range-slider': '0;10000'}

    -- unparsed_obj argument is JSON array with filter box parameters
    """

    # Nested dict comprehension
    parsed_obj = { key:value for (key, value) in [o.values() for o in unparsed_obj] }

    return parsed_obj


class Bonus(models.Model):
    '''
    Bonus entity
    e.g. 100% No dep bonus by 365bet...
    '''

    # Mapping filters to Q objects
    _FILTER_LIST = {
        'sorting': {
            'bon_max_to_min': 'dep',
            'bon_min_to_max': '-dep',
            'dep_min_to_max': 'bonus_digit',
            'dep_max_to_min': '-bonus_digit',
            'doa_old_to_new': 'doa',
            'doa_new_to_old': '-doa',
            'wager_min_to_max': 'wager',
            'wager_max_to_min': '-wager',
            # 'ttl_min_to_max': 'ttl',
            # 'ttl_max_to_min': '-ttl',
        },

        'type': {
            'casino': Q(suplier__suplier_type=0),
            'betting': Q(suplier__suplier_type=1),
        },

        # ?Checkboxes
        'nodep': Q(dep_bool=False),  
        'license': Q(suplier__ca_license_bool=True),
        # 'safe': ,
        # 'fresh':,
        
        # ? If you wanna add new filter/sorting. ADD HERE.
    }

    two_word_desc = models.CharField(max_length=300, blank=False, verbose_name="About the bonus in 2 words")    
    
    # If we have freespin for example, the value should be equals zero
    bonus_digit = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(1000000)],\
        verbose_name="Bonus value")
    bonus_desc = models.TextField(max_length=1500, blank=True, null=True, verbose_name="Bonus description")
    suplier = models.ForeignKey(Suplier, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='bonus_images/', blank=True, null=True, verbose_name='Bonus image')

    # Deposit or non-dep 
    dep_bool = models.BooleanField(default=True, blank=False)
    dep = models.PositiveSmallIntegerField(blank = False)

    # Date of adding
    doa = models.DateField(default=datetime.date.today, verbose_name="Date of adding")
    # Date of expiring    
    doe = models.DateField(default=today_plus_30_days, verbose_name="Date of expiring")

    wager = models.SmallIntegerField(default=0, blank=True, \
        validators=[MaxValueValidator(100)], verbose_name='Bonus wager')
    bonus_type = models.IntegerField(choices=BONUS_TYPES, default=0)

    # Shows time-to-live of bonus(how much time you have to use the bonus till it expires)
    # Checks DOE is not less than DOA. Returns datetime.date
    def ttl_full(self):
        try:
            # If Date of expiring for some reasons is earlier than date of adding
            #   - it equals DOE value to DOA value. So ttl is 0, but it will bypass a bunch of issues
            if self.doe < self.doa:
                self.doe = self.doa
                self.save()

            ttl_obj = self.doe - self.doa
            return ttl_obj
        except:
            return 0

    # Time to live of a bonus in days
    def ttl_days(self):
        date_object = self.ttl_full()
        return date_object.days

    # Time to live of a bonus in hours
    def ttl_hours(self):
        date_object = self.ttl_full()
        return date_object.days * 24

    # Returns related bonuses to our suplier instance
    def get_other_bonuses(self):
        return self.suplier.bonus_set.all()

    @staticmethod
    def create_mock(amount):
        """
        Creates mock bonus object        
        """
        pass

    @classmethod
    def filtering(cls, parsed_JSON):
        """
        Implementation of Filter Box filtering 

        # FILTERING ROADMAP:
        #
        # 1) We gotta filter by selected Bonus type(Casino/Betting/All...)
        # 2) Apply checkboxes
        # 3) Aplly Range sliders params(wager, bonus, deposit)
        # 4) Sorting result queryset
        #
        # SCHEME OF FILTERING. The order is vital 
        #   TYPE -> CHECKBOXES -> RANGE SLIDERS -> SORTING ----> Result queryset 
        """    

        # Type checking 
        # !Type checking section gotta occurs first in the order
        # Fetches Bonuses by certain type. Returns QuerySet with Bonuses taken by filter 'type'
        # e.g. Casino/Betting/All. Fetches all Casino Suplier instances(all casinos in current DB)
        if 'type' in parsed_JSON and parsed_JSON['type'] != 'all':
            # _ is just decoration 
            _ = parsed_JSON['type']
            result_queryset = cls.objects.filter(cls._FILTER_LIST['type'][_])
            
        # Happens if 'type' is 'all' or something got wrong
        else:
            result_queryset = cls.objects.all()

        # Apply checkboxes for Bonus model
        # TODO Make checkbox filtering using for loop. Example below
        # for checkbox in cls._FILTER_LIST['checkbox'].items():
        #     if checkbox in parsed_JSON:
        #         pass
        #     pass

        # License checking
        if 'license' in parsed_JSON:
            result_queryset = result_queryset.filter(cls._FILTER_LIST['license'])

        # Nodep checking 
        if 'nodep' in parsed_JSON:
            result_queryset = result_queryset.filter(cls._FILTER_LIST['nodep'])
        
        #? Create below any checkbox filters if you want so

        #? /
 
        # Range sliders. Apply range slider filters
        result_queryset = result_queryset.filter( 
            Q(wager__range = parsed_JSON['wager-js-range-slider'].split(';')) &\
            Q(dep__range = parsed_JSON['deposit-js-range-slider'].split(';')) &\
            Q(bonus_digit__range = parsed_JSON['bonus-js-range-slider'].split(';')) \
            # If you wanna add a new range-slider, just add below

        )
        # Sorting. Sorting gotta occurs after all filters in the order
        result_queryset = result_queryset.order_by(cls._FILTER_LIST['sorting'][parsed_JSON['sorting']])
        
        return result_queryset


    @classmethod
    def get_filtered_bonuses(cls, unparsed_JSON):
        # Bonus filtering
        # Fetchs Bonus queryset by filter params from unparsed_JSON
        # -- unparsed_JSON - JSON Array with filter params
    
        # Input data should be parsed(by parsingObject function, see above) JSON object
        # {'sorting': 'dep_min_to_max', 'type': 'all', 'wager-js-range-slider': '0;42',
        #  'bonus-js-range-slider': '0;5000', 'deposit-js-range-slider': '0;10000'}
    
        # Parsing unparsed_json. Obj is readable now for filtering method  
        obj = get_parsed_json(unparsed_JSON)

        # Returns Bonus queryset by filter params from parsed JSON    
        result_query = cls.filtering(obj)

        return result_query

    @classmethod
    def get_searched_bonuses(cls, search_input):
        # Bonus searching for Search Input
        # -- search_input - search input value(e.g. 'TTR Casinso'...etc)

        bonuses_result = cls.objects.filter(
            Q(two_word_desc__icontains=search_input)
                | Q(bonus_desc__icontains=search_input)
                | Q(bonus_digit__icontains=search_input)
                | Q(dep__icontains=search_input)
                # Q object for suplier title 
                | Q(suplier__title__icontains=search_input)
            )
        
        # Returns Bonus queryset by search input
        return bonuses_result

    @classmethod
    def get_wager_max(cls):
        return Bonus.objects.aggregate(Max('wager'))['wager__max']

    @classmethod
    def get_bonus_max(cls):
        return Bonus.objects.aggregate(Max('bonus_digit'))['bonus_digit__max']

    @classmethod
    def get_dep_max(cls):
        return Bonus.objects.aggregate(Max('dep'))['dep__max']

    class Meta:
        ordering = ['-bonus_digit']

    def __str__(self):
        return f'{self.suplier.title} : {self.two_word_desc}'


# Returns metadata(like max amount of nodep bonuses...etc) dict for filterbox
def filterbox_meta_count():
    # ! Reassign this var to empty dict
    filter_box_meta = {
        'nodep_count' : 12,
        'license_count' : 25,
        'safe_count' : 42,
        'fresh_count' : 6,
        'season_count' : 2,
        
        'all' : 300,
        'casino': 154,
        'betting': 25,

        'wager_range_max' : 150,
        'bonus_range_max' : 4000,
        'dep_range_max' : 12540,
    }

    filter_box_meta['nodep_count'] = Bonus.objects.filter(Q(dep_bool=False)).count()
    filter_box_meta['license_count'] = Bonus.objects.filter(Q(suplier__ca_license_bool=True)).count()
    filter_box_meta['fresh_count'] = Bonus.objects.filter(Q(doa__gt=datetime.date.today() - datetime.timedelta(days=7))).count()

    filter_box_meta['all'] = Bonus.objects.all().count()
    filter_box_meta['casino'] = Bonus.objects.filter(Q(suplier__suplier_type=0)).count()
    filter_box_meta['betting'] = Bonus.objects.filter(Q(suplier__suplier_type=1)).count()

    # TODO Replace maxes below into Bonus methods and cover by @property. Check out how the decision will work with Serializer default
    filter_box_meta['wager_range_max'] = Bonus.objects.aggregate(Max('wager'))['wager__max'] or 0
    filter_box_meta['bonus_range_max'] = Bonus.objects.aggregate(Max('bonus_digit'))['bonus_digit__max'] or 0
    filter_box_meta['dep_range_max'] = Bonus.objects.aggregate(Max('dep'))['dep__max'] or 0

    return filter_box_meta