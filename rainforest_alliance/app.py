import csv
import datetime
import re
import logging

# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#region certificate_holders checking rules
def check_certificate_holder_id(data):
    pattern = r'^[A-Za-z0-9]+$'
    return re.match(pattern, data) is not None

def check_certificate_id(data):
    pattern = r'^[A-Za-z0-9]+$'
    return re.match(pattern, data) is not None

def check_country(data):
    valid_country = ['Country A', 'Country B', 'Country C', 'Country D']
    return data.strip() in valid_country

def check_certificate_type(data):
    valid_certificate_type = ['Single Farm', 'Multi Farm', 'Group Of Mixed Farms', 'Group Of Small Farms', 'Single Site']
    return data.strip() in valid_certificate_type

def check_certificate_date(start_date, end_date):
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Define valid range for certificates
    valid_range_start = datetime.datetime.strptime('1980-01-01', '%Y-%m-%d')
    # Based on Rainforest Alliance, certificates are valid for a maximum of 3 years
    valid_range_end = datetime.datetime.now() + datetime.timedelta(days=3*365)
    
    # Check if start_date and end_date can be parsed as valid datetime format
    try:
        start_datetime = datetime.datetime.strptime(start_date, date_format)
        end_datetime = datetime.datetime.strptime(end_date, date_format)
    except ValueError:
        logging.error('Date parsing failed for row: start_date=%s, end_date=%s', start_date, end_date)
        return False
    
    # Check if start_date is smaller than end_date
    if start_datetime >= end_datetime:
        logging.error('Invalid Certificate Dates for row: start_date=%s, end_date=%s', start_date, end_date)
        return False
    
    # Check if start_date and end_date are within the valid range
    if start_datetime < valid_range_start or end_datetime > valid_range_end:
        logging.error('Certificate dates out of valid range for row: start_date=%s, end_date=%s', start_date, end_date)
        return False
    
    return True
#endregion

#region volume_and_crops checking rules
def check_certificate_holder_id(data):
    pattern = r'^[A-Za-z0-9]+$'
    return re.match(pattern, data) is not None

def check_certificate_id(data):
    pattern = r'^[A-Za-z0-9]+$'
    return re.match(pattern, data) is not None

def check_crop(data):
    valid_crop = ['Cocoa', 'Coffee', 'Tea']
    return data.strip() in valid_crop

def check_positive_volume(data):
        return data > 0
#endregion

def process_certificate_holders_csv(input_file, validated_file, check_file):
    try:
        with open(input_file, 'r') as csvfile, \
                open(validated_file, 'w', newline='') as validated, \
                open(check_file, 'w', newline='') as need_check:
            reader = csv.DictReader(csvfile)
            writer_validated = csv.DictWriter(validated, fieldnames=reader.fieldnames)
            writer_need_check = csv.DictWriter(need_check, fieldnames=reader.fieldnames + ['Error'])
            writer_validated.writeheader()
            writer_need_check.writeheader()
            
            for row_num, row in enumerate(reader, start=1):
                errors = []
                # Check if any column is empty or null
                for key, value in row.items():
                    if not value.strip():
                        errors.append(f'{key} is empty')
                
                # Check Certificate Holder ID format (if needed)
                if 'Certificate Holder ID' in row and not check_certificate_holder_id(row['Certificate Holder ID']):
                    errors.append('Invalid Certificate Holder ID')
                
                # Check Certificate ID format (if needed)
                if 'Certificate ID' in row and not check_certificate_id(row['Certificate ID']):
                    errors.append('Invalid Certificate ID')
                
                # Check Country format
                if 'Country' in row and not check_country(row['Country']):
                    errors.append('Invalid Country')
                
                # Check Certificate Type format
                if 'Certificate Type' in row and not check_certificate_type(row['Certificate Type']):
                    errors.append('Invalid Certificate Type')
                
                # Check Certificate Dates
                if not check_certificate_date(row['Certificate start date'], row['Certificate end date']):
                    errors.append('Invalid Certificate Dates')
                
                if errors:
                    row_with_errors = row.copy()
                    row_with_errors['Error'] = ', '.join(errors)
                    writer_need_check.writerow(row_with_errors)
                else:
                    writer_validated.writerow(row)
    except Exception as e:
        logging.error('Error processing CSV file: %s', e)

def process_volume_and_crops_csv(input_file, validated_file, check_file):
    try:
        with open(input_file, 'r') as csvfile, \
                open(validated_file, 'w', newline='') as validated, \
                open(check_file, 'w', newline='') as need_check:
            reader = csv.DictReader(csvfile)
            writer_validated = csv.DictWriter(validated, fieldnames=reader.fieldnames)
            writer_need_check = csv.DictWriter(need_check, fieldnames=reader.fieldnames + ['Error'])
            writer_validated.writeheader()
            writer_need_check.writeheader()
            
            for row_num, row in enumerate(reader, start=1):
                errors = []
                # Check if any column is empty or null
                for key, value in row.items():
                    if not value.strip():
                        errors.append(f'{key} is empty')
                
                # Check Certificate Holder ID format (if needed)
                if 'Certificate Holder ID' in row and not check_certificate_holder_id(row['Certificate Holder ID']):
                    errors.append('Invalid Certificate Holder ID')
                
                # Check Certificate ID format (if needed)
                if 'Certificate ID' in row and not check_certificate_id(row['Certificate ID']):
                    errors.append('Invalid Certificate ID')
                
                # Check Crop format
                if 'Country' in row and not check_crop(row['Crop']):
                    errors.append('Invalid Crop')
                
                # Check Estimated harvested volume format
                if 'Estimated harvested volumn' in row and not check_positive_volume(row['Estimated harvested']):
                    errors.append('Invalid Estimated harvested volumn')
                
                if errors:
                    row_with_errors = row.copy()
                    row_with_errors['Error'] = ', '.join(errors)
                    writer_need_check.writerow(row_with_errors)
                else:
                    writer_validated.writerow(row)
    except Exception as e:
        logging.error('Error processing CSV file: %s', e)


def main():
    try:
        input_file = './input_data/certificate_holders_input.csv'
        validated_file = './output_data/certificate_holders_validated.csv'
        need_check_file = './output_data/certificate_holders_need_check.csv'
        
        process_certificate_holders_csv(input_file, validated_file, need_check_file)

        input_file = './input_data/volume_and_crops_input.csv'
        validated_file = './output_data/volume_and_crops_validated.csv'
        need_check_file = './output_data/volume_and_crops_need_check.csv'
        
        process_volume_and_crops_csv(input_file, validated_file, need_check_file)

    except Exception as e:
        logging.error('An error occurred in main function: %s', e)

if __name__ == "__main__":
    main()
