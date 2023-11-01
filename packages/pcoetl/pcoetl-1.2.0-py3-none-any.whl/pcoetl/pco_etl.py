### ETL script to return data from the Planning Center API


class pco_etl:
    def __init__(self, app_id, secret):
        ''' Authenticate PCO API with Personal Access Token'''
        self.app_id = app_id
        self.secret = secret
    
    def extract_data(self, api):

        import requests

        import json

        import pandas as pd
        

        api_base='https://api.planningcenteronline.com'

        api_url = api_base + api

        #session = requests.Session()
        r = requests.get(api_url, auth=(self.app_id, self.secret))
        pco_data = r.json()
        
        pco_data_output = pco_data["data"]
    
        try: 
            if list(pco_data['links'].keys())[1] == 'next':
                try:
                    while pco_data['links']['next']:
                        try:
                            res = requests.get(pco_data['links']['next'], auth=(self.app_id, self.secret))
                            res = res.text
                            res = res.replace("null", '"NO_DATA"')
                            res = res.replace("[]", '"NO_DATA"')
                            pco_data = json.loads(res)
                            pco_data_output.extend(pco_data["data"])
                
                        except:
                            pass         
                except:
                    pass      
        except:
            pass
                
        r.close()

        return pd.DataFrame(pco_data_output)
    
    def expand_dataset(data):
        from pandas import json_normalize
        from pandas import merge
        
        try:
            
            cols = ['attributes', 'relationships', 'links']
            
            base_data = data[['type', 'id']]
            
            for i in cols:
                temp_df = json_normalize(data[i])
                
                base_data = merge(
                    left = base_data,
                    right = temp_df,
                    left_index = True,
                    right_index = True
                )
        except:
            
            cols = ['attributes', 'links']
            
            base_data = data[['type', 'id']]
            
            for i in cols:
                temp_df = json_normalize(data[i])
                
                base_data = merge(
                    left = base_data,
                    right = temp_df,
                    left_index = True,
                    right_index = True
                )

        return base_data
  
    def get_pco_include(self, api):

        import requests

        import json

        import pandas as pd
        

        api_base='https://api.planningcenteronline.com'

        api_url = api_base + api

        #session = requests.Session()
        r = requests.get(api_url, auth=(self.app_id, self.secret))
  
        pco_data = r.json()
        
        pco_data_output = pco_data["included"]

        try: 
            if list(pco_data['links'].keys())[1] == 'next':
                try:
                    while pco_data['links']['next']:
                        try:
                            res = requests.get(pco_data['links']['next'], auth=(self.app_id, self.secret))
                            res = res.text
                            res = res.replace("null", '"NO_DATA"')
                            res = res.replace("[]", '"NO_DATA"')
                            pco_data = json.loads(res)
                            pco_data_output.extend(pco_data["included"])
                        except:
                            pass        
                except:
                    pass  
        except:
            pass
                
        r.close()

        return pd.DataFrame(pco_data_output)
    
    def load_people_api(self):
        """ Function loads people data using given authentication"""
        import pandas as pd
        import numpy as np
        from datetime import datetime
        people_api = '/people/v2/people?per_page=100&include=addresses'
        
        people_data = pco_etl.extract_data(self, api = people_api)
        
        people_data = pco_etl.expand_dataset(people_data)
        
        # Get address IDs
        exploded_address_ids = people_data[['id', 'addresses.data']].explode('addresses.data')

        address_ids = []

        for i in range(len(exploded_address_ids[['addresses.data']])):
            try:
                address_ids.append(exploded_address_ids['addresses.data'].iloc[i].pop('id'))
            except:
                address_ids.append('NO_DATA')
                
        id_address = pd.DataFrame(address_ids)
        id_address.name = 'address_id'
        
        people_data = pd.merge(
                            left=people_data,
                            right=id_address,
                            left_index=True,
                            right_index=True
                        )

        people_data.rename(
            columns={
                people_data.iloc[:, -1].name: 'address_id'
            },
            inplace=True)
        
        
        # drop unimportant and sensitive columns
        people_data.drop(columns=['type',
                                  'self', 
                                  'html',
                                  'avatar',
                                  'demographic_avatar_url',
                                  'first_name',
                                  'given_name',
                                  'last_name', 
                                  'middle_name', 
                                  'name', 
                                  'nickname',
                                  'gender.data',
                                  'directory_status',
                                  'primary_campus.data', 
                                  'gender.data.type',
                                  'gender.data.id', 
                                  'addresses.links.related', 
                                  'addresses.data',
                                  'primary_campus.data.type',], inplace=True)
        
        # rename columns
        people_data.rename(
            columns={
                'id': 'people_id',
                'accounting_administrator': 'accounting_administrator_status', 
                'anniversary': 'anniversary_date', 
                'birthdate': 'birthday_date', 
                'can_create_forms': 'can_create_forms_status', 
                'can_email_lists': 'can_email_lists_status', 
                'child': 'is_child_status',
                'created_at': 'created_date', 
                'gender': 'gender', 
                'grade':'child_grade', 
                'graduation_year': 'child_graduation_year',
                'inactivated_at': 'inactivated_date', 
                'medical_notes': 'medical_notes', 
                'membership': 'membership',
                'passed_background_check': 'passed_background_check_status',
                'people_permissions': 'people_permissions', 
                'remote_id': 'remote_id', 
                'school_type': 'child_school_type', 
                'site_administrator': 'site_administrator_staus',
                'status': 'active_status', 
                'updated_at': 'updated_date', 
                'primary_campus.data.id': 'campus_id', 
                'address_id': 'address_id',
            },
            inplace=True)
        
        
        # set date data types
        people_data['anniversary_date'] = pd.to_datetime(people_data['anniversary_date'], errors='coerce').dt.strftime('%Y/%m/%d')
        people_data['birthday_date'] = pd.to_datetime(people_data['birthday_date'], errors='coerce').dt.strftime('%Y/%m/%d')
        people_data['created_date'] = pd.to_datetime(people_data['created_date'], errors='coerce').dt.strftime('%Y/%m/%d')
        people_data['inactivated_date'] = pd.to_datetime(people_data['inactivated_date'], errors='coerce').dt.strftime('%Y/%m/%d')
        people_data['updated_date'] = pd.to_datetime(people_data['updated_date'], errors='coerce').dt.strftime('%Y/%m/%d')
        
        people_data['anniversary_date'] = pd.to_datetime(people_data['anniversary_date'], errors='coerce')
        people_data['birthday_date'] = pd.to_datetime(people_data['birthday_date'], errors='coerce')
        people_data['created_date'] = pd.to_datetime(people_data['created_date'], errors='coerce')
        people_data['inactivated_date'] = pd.to_datetime(people_data['inactivated_date'], errors='coerce')
        people_data['updated_date'] = pd.to_datetime(people_data['updated_date'], errors='coerce')
        
        # replace "NO_DATA" and None with np.nan values
        people_data.replace('NO_DATA', np.nan, inplace=True)
        
        # fillna for campus id based on rule
        if people_data.campus_id.nunique() == 1:
            people_data['campus_id'] = people_data['campus_id'].fillna(method='ffill').fillna(method='bfill')
    
        # calculate age, tenure, update, and marriage lengths
        today = pd.Timestamp.now().floor('d')

        people_data['person_age_yrs'] = (today - people_data['birthday_date'])/np.timedelta64(1, 'Y')
        people_data['person_marriage_length_yrs'] = (today - people_data['anniversary_date'])/np.timedelta64(1, 'Y')
        people_data['person_tenure_yrs'] = (today - people_data['created_date'])/np.timedelta64(1, 'Y')
        people_data['person_last_update_yrs'] = (today - people_data['updated_date'])/np.timedelta64(1, 'Y')
        
        # calculate age, tenure and marriage lengths for inactivated people
        people_data['person_age_inactive'] = (people_data['inactivated_date'] - people_data['birthday_date'])/np.timedelta64(1, 'Y')
        people_data['person_marriage_length_inactive'] = (people_data['inactivated_date'] - people_data['anniversary_date'])/np.timedelta64(1, 'Y')
        people_data['person_tenure_inactive'] = (people_data['inactivated_date'] - people_data['created_date'])/np.timedelta64(1, 'Y')
        
        # replace calculated values when inactive
        people_data.loc[people_data['active_status'] == 'inactive', 'person_age_yrs'] = people_data['person_age_inactive']
        people_data.loc[people_data['active_status'] == 'inactive', 'person_marriage_length_yrs'] = people_data['person_marriage_length_inactive']
        people_data.loc[people_data['active_status'] == 'inactive', 'person_tenure_yrs'] = people_data['person_tenure_inactive']
        
        # drop inactive columns as they are now placed properly
        people_data.drop(
            columns=[
                'person_age_inactive',
                'person_marriage_length_inactive',
                'person_tenure_inactive',
                ], 
            inplace=True)
        
        people_data['Age Group'] = "Senior"
        people_data.loc[people_data['person_age_yrs'] < 18, 'Age Group'] = "Child"
        people_data.loc[people_data['person_age_yrs'] >= 18, 'Age Group'] = "Young Adult"
        people_data.loc[people_data['person_age_yrs'] >= 30, 'Age Group'] = "Adult"
        people_data.loc[people_data['person_age_yrs'] >= 45, 'Age Group'] = "Middle Aged"
        people_data.loc[people_data['person_age_yrs'] >= 65, 'Age Group'] = "Senior"

        return people_data
    
    def load_giving_api(self):
        """ Function loads giving data using given authentication"""
        import pandas as pd
        import numpy as np
        from datetime import datetime
        giving_api = '/giving/v2/donations?include=designations&per_page=100'
        
        giving_data = pco_etl.extract_data(self, api = giving_api)
        
        giving_data = pco_etl.expand_dataset(giving_data)
        
        # Get designation IDs
        exp_d = giving_data[['id', 'designations.data']].explode('designations.data')
        id_designation = pd.DataFrame(exp_d['designations.data'].tolist())['id']
        id_designation.name = 'id_designation'
        exp_d.reset_index(inplace=True)
        exp_d = pd.merge(
            left=exp_d,
            right=id_designation,
            left_index=True,
            right_index=True
        )


        exp_d.drop(columns=['designations.data', 'index'],inplace=True)
        # Join designation IDs back to the donations table
        giving_data = pd.merge(
            left=giving_data,
            right=exp_d,
            left_on='id',
            right_on='id',
            how='left'
        )
        
        donations_des = pco_etl.get_pco_include(self, api = giving_api)
        donations_des_exp = pco_etl.expand_dataset(donations_des)
        
        # ensure only designations come through (this probably won't ever do anything but is more of a fail safe)
        donations_des_exp = donations_des_exp[donations_des_exp['type'] == 'Designation']

        # select needed columns and rename
        donations_des_exp = donations_des_exp[['id', 'fund.data.id', 'amount_cents']]
        donations_des_exp.rename(columns={
            'id': 'id_designation',
            'fund.data.id': 'fund_id',
            'amount_cents': 'alloc_amount_cents'
        },
                                inplace=True)

        # Join designation back to the giving table
        giving_data = pd.merge(
            left=giving_data,
            right=donations_des_exp,
            left_on='id_designation',
            right_on='id_designation',
            how='left'
        )
        
        # select needed columns
        giving_data = giving_data[[
            'id','completed_at', 'amount_cents',
            'created_at', 'fee_cents', 'payment_brand',
            'payment_method', 'payment_method_sub', 'payment_status', 'received_at',
            'refundable', 'refunded', 'updated_at', 'person.data.id', 'payment_source.data.id', 
            'recurring_donation.data.id','batch.data.id', 'id_designation', 
            'fund_id', 'alloc_amount_cents']]

        # rename the columns
        giving_data.rename(
            columns={
                'id': 'donation_id', 
                'completed_at': 'completed_date',
                'created_at': 'created_date', 
                'fee_cents': 'donation_fee_cents', 
                'received_at': 'received_date',
                'updated_at': 'updated_date', 
                'person.data.id': 'people_id',
                'payment_source.data.id': 'payment_source_id', 
                'recurring_donation.data.id': 'recurring_donation_id',
                'batch.data.id': 'batch_id',
                'id_designation': 'designation_id', 
                'alloc_amount_cents': 'donation_amount_cents',         
            },
            inplace=True
        )
        
        # fee % allocation
        giving_data['fee_percentage'] = giving_data['donation_fee_cents'] / giving_data['amount_cents']
        giving_data['fee_percentage'] = giving_data['fee_percentage'].abs()

        giving_data['donation_fee_cents'] = giving_data['donation_amount_cents'] * giving_data['fee_percentage']

        # calculate dollar amounts
        giving_data['donation_fee_dollars'] = giving_data['donation_fee_cents']/100
        giving_data['donation_amount_dollars'] = giving_data['donation_amount_cents']/100
        giving_data['amount_dollars'] = giving_data['amount_cents']/100
        # get recurring Donations 
        giving_data['donation_type'] = "Recurring" 
        giving_data.loc[giving_data['recurring_donation_id'].isna(), 'donation_type'] = 'NonRecurring'
        giving_data.drop(columns=['recurring_donation_id'], inplace=True)
        
        # get refunds
        def refund_data(x):
            if x == True:
                return -1
            else:
                return 1
            
        giving_data['refunded'] = giving_data['refunded'].apply(refund_data)
        giving_data['donation_amount_dollars'] = giving_data['donation_amount_dollars'] * giving_data['refunded']
        giving_data['donation_amount_cents'] = giving_data['donation_amount_cents'] * giving_data['refunded']
        giving_data['amount_dollars'] = giving_data['amount_dollars'] * giving_data['refunded']


        # Net donations
        giving_data['donation_net_amount_dollars'] = giving_data['donation_amount_dollars'] - giving_data['donation_fee_dollars']
        
        # clean dates
        giving_data['completed_date'] = pd.to_datetime(giving_data['completed_date'], errors='coerce')
        giving_data['created_date'] = pd.to_datetime(giving_data['created_date'], errors='coerce')
        giving_data['received_date'] = pd.to_datetime(giving_data['received_date'], errors='coerce')
        giving_data['updated_date'] = pd.to_datetime(giving_data['updated_date'], errors='coerce')
        
        return giving_data
    
    def load_fund_api(self):
        """ Function loads fund data using given authentication"""
        import pandas as pd
        import numpy as np
        from datetime import datetime
        funds_api = '/giving/v2/funds?per_page=100'
        # get funds data
        funds_data = pco_etl.extract_data(self, api = funds_api)
        
        funds_data = pco_etl.expand_dataset(funds_data)
        
        funds_data = funds_data[['id', 'name']]
        funds_data.rename(columns={
            'id': 'fund_id',
            'name': 'fund_name'
        },
                    inplace = True)
        
        return funds_data
    
    def load_campus_api(self):
        """ Function loads campus data using given authentication"""
        import pandas as pd
        import numpy as np
        from datetime import datetime
        campus_api = '/giving/v2/campuses?per_page=100'
        
        campus_data = pco_etl.extract_data(self, api = campus_api)
        
        campus_data = pco_etl.expand_dataset(campus_data)
        
        campus_data = campus_data[['id', 'name', 'address.street_line_1', 'address.street_line_2', 'address.city', 'address.state', 'address.zip']]
        campus_data.rename(columns={
            'id': 'campus_id',
            'name': 'campus_name',
            'address.street_line_1': 'street_line_1',
            'address.street_line_2': 'street_line_2',
            'address.state': 'state',
            'address.zip': 'zip_code',
        },
                    inplace = True)
        
        return campus_data
        
    def load_address_api(self):
        """ Function loads address data using given authentication"""
        import pandas as pd
        import numpy as np
        from datetime import datetime
        address_api = '/people/v2/addresses?per_page=100'
        
        address_data = pco_etl.extract_data(self, api = address_api)
        
        address_data = pco_etl.expand_dataset(address_data)
        
        address_data = address_data[address_data['primary'] == True]

        address_data = address_data[['id', 'city', 'state', 'street', 'zip']]

        address_data.rename(
            columns={
                'id': 'address_id', 
                'city': 'city',
                'state': 'state',
                'street': 'street_line_1',
                'zip': 'zip_code'
            },
            inplace=True
        )
        address_data['street_line_1'] = address_data['street_line_1'].str.replace("\n", "")
        
        return address_data
        
     
    def load_field_api(self):
        """ Function loads field data using given authentication"""
        import pandas as pd
        import numpy as np
        from datetime import datetime
        field_api = '/people/v2/field_data?per_page=100'
        
        api_def = '/people/v2/field_definitions?per_page=100'
        
        field_data = pco_etl.extract_data(self, api = field_api)
        
        field_data = pco_etl.expand_dataset(field_data)   
        
        field_definitions = pco_etl.extract_data(self, api = api_def)
        
        field_definitions = pco_etl.expand_dataset(field_definitions) 
        
        # Prep Field Data Table
        field_data_table = pd.merge(
            left = field_data,
            right = field_definitions,
            left_on = 'field_definition.data.id',
            right_on = 'id',
            how = 'left'
        )

        field_data_table.replace({"NO_DATA":np.NaN}, inplace=True)


        field_data_table = field_data_table[['name', 'data_type', 'value', 'customizable.data.id']]

        field_data_table.rename(
            columns={
                'name': 'activity',
                'value': 'date',
                'customizable.data.id': 'people_id'
            },
            inplace = True
        )

        field_data_table = field_data_table[field_data_table['data_type'] == 'date']

        field_data_table.drop(columns=['data_type'], inplace=True)

        field_data_table['date'] = pd.to_datetime(field_data_table['date'], errors='coerce')
        
        return field_data_table
    
    def load_checkins_api(self):
        """ Function loads field data using given authentication"""
        import pandas as pd
        import numpy as np
        from datetime import datetime
        
        checkins_api = '/check-ins/v2/check_ins?per_page=100'
        checkinsinclude_api = '/check-ins/v2/check_ins?per_page=100&include=event_period'
        
        checkin_data = pco_etl.extract_data(self, api = checkins_api)
        
        checkin_data = pco_etl.expand_dataset(checkin_data) 
        
        # select needed columns
        checkin_data = checkin_data[['id', 'checked_out_at', 'confirmed_at', 'created_at',
                                 'kind', 'one_time_guest', 'updated_at', 'event_period.data.id','person.data.id']] 
        
        # rename columns
        checkin_data.rename(
            columns={
                'id': 'checkin_id',
                'checked_out_at': 'checked_out_date',
                'confirmed_at': 'confirmed_date',
                'created_at': 'created_date',
                'kind': 'checkin_type',
                'updated_at': 'updated_date',
                'event_period.data.id': 'event_period_id',
                'person.data.id': 'people_id'
            },
            inplace=True
        )

        checkin_data['checked_out_date'] = pd.to_datetime(checkin_data['checked_out_date'], errors='coerce')
        checkin_data['confirmed_date'] = pd.to_datetime(checkin_data['confirmed_date'], errors='coerce')
        checkin_data['created_date'] = pd.to_datetime(checkin_data['created_date'], errors='coerce')
        checkin_data['updated_date'] = pd.to_datetime(checkin_data['updated_date'], errors='coerce')
        
        event_period_ids = pco_etl.get_pco_include(self, api = checkinsinclude_api)
        event_period_ids = pco_etl.expand_dataset(event_period_ids)
        
        event_period_ids = event_period_ids[['id','event.data.id']]
        
        event_period_ids.rename(
            columns={
                'id': 'event_period_id',
                'event.data.id': 'event_id'
            },
            inplace=True
        )
        
        checkin_data = pd.merge(
            left=checkin_data,
            right=event_period_ids,
            on = 'event_period_id',
            how='left'
        )
        
        return checkin_data
    
    def load_event_api(self):
        """ Function loads field data using given authentication"""
        import pandas as pd
        import numpy as np
        from datetime import datetime
        events_api = '/check-ins/v2/events'

        event_data = pco_etl.extract_data(self, api = events_api)
        
        event_data = pco_etl.expand_dataset(event_data) 
        
        event_data = event_data[['id', 'name', 'frequency']]
        
        event_data.rename(
            columns={
                'id': 'event_id',
                'name': "event_name",
                'frequency': 'event_frequency'
            },
            inplace=True
        )
        
        event_data['event_frequency'] = event_data['event_frequency'].replace('None', 'Once')
        
        return event_data