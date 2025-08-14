import csv
import sys
import os

def referenceData(contestList, contestStatus):
    contestList = {}
    contestStatus = {}

    # load contestList
    try:
        with open(contestList, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                contestList[row['short-name']] = row
    except Exception as e:
        print(f"Error loading contestList: {e}")
    
    # load contestStatus
    try:
        with open(contestStatus, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                key = f"{row['short-name']}_{row['year']}"
                contestStatus[key] = row

    except Exception as e:
        print(f"Error loading contestStatus: {e}")
    
    return contestList, contestStatus

# check if contestList is valid
def checkContestList(filePath, referenceData):
    errors = []

    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            # required columns: region-name	full-name	short-name
            required = ['region-name', 'full-name', 'short-name']
            if not all(col in reader.fieldnames for col in required):
                errors.append("Missing required columns in contestList")
                return errors
            
            # check each row
            for lineNum, row in enumerate(reader, start=2):
                shortName = row['short-name']
                if shortName in referenceData:
                    refShortName = referenceData[shortName]
                    if row['region-name'] != refShortName['region-name']:
                        errors.append(f"Wrong region name for {shortName} on line: {lineNum}")
                    if row['full-name'] != refShortName['full-name']:
                        errors.append(f"Wrong full name for {shortName} on line: {lineNum}")
                    
    except Exception as e:
        errors.append(f"Cannot read file: {e}")

    return errors

# check if contestStatus is valid
def checkContestStatus(filePath, referenceData):
    errors = []

    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            # required colums: short-name	year	count	statements	data	solutions	packages
            required = ['short-name', 'year', 'count', 'statements', 'data', 'solutions', 'packages']
            if not all(col in reader.fieldnames for col in required):
                errors.append("Missing required columns in contestStatus")
                return errors
        
            # check each row
            for lineNum, row in enumerate(reader, start=2):
                shortName_year = f"{row['short-name']}_{row['year']}"
                if shortName_year in referenceData:
                    ref_shortName_year = referenceData[shortName_year]
                    if row['count'] != ref_shortName_year['count'] and row['count'] != '?' and ref_shortName_year['count'] != '?':
                        errors.append(f"Wrong count value for {row['short-name']} {row['year']} on line: {lineNum}")
                    # check boolean fields -> statements, data, solutions, packages
                    for field in ['statements', 'data', 'solutions', 'packages']:
                        if row[field].upper() not in ['TRUE', "FALSE"]:
                            errors.append(f"Must be in TRUE/FALSE: line {lineNum}")
    except Exception as e:
        errors.append(f"Cannot read file: {e}")

    return errors

# determine if inputted tsv file is contestList or contestStatus
def fileTypeCheck(filePath):
    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            header = next(reader)

            if 'short-name' in header and 'year' in header and 'count' in header:
                return 'contest-status'
            if 'region-name' in header and 'full-name' in header and 'short-name' in header:
                return 'contest-list'
            else:
                return 'unknown'
    except:
        return 'unknown'

# can run file with python3 tsvVerifer.py file-to-check.tsv
def main():
    if len(sys.argv) < 2:
        print("Ensure correct usage: python3 tsvVerifier.py <file-to-check.tsv>")
        sys.exit(1)
    
    checkingFile = sys.argv[1]
    if not os.path.exists(checkingFile):
        print(f"File: {checkingFile} does not exist in directory")
        sys.exit(1)
    
    contestList, contestStatus = referenceData('ContestList copy.tsv', 'ContestStatus copy.tsv')
    fileType = fileTypeCheck(checkingFile)

    if fileType == 'contest-list':
        errors = checkContestList(fileType)
    
    elif fileType == 'contest-status':
        errors = checkContestStatus(fileType)
    else:
        print("Could not determine file type")
        sys.exit(1)
    
    if errors:
        print(f"Found {len(errors)} errors")
        for error in errors:
            print(f"    -> {error}")
        sys.exit(1)
    else:
        print("0 Errors Found")
        sys.exit(0)
    
if __name__ == "__main__":
    main()
    
