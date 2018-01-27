from pprint import pprint
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import json

#SSID = '1HycKCpeWvcn0H_N69BOODK28TRehSNqWiOjJ-E-Tyj0' #KINNICK SOCIETY
# SSID = '1JFcbPRrtorRyv8PVgjkBsLtbchiChb6q7IqevorF2-4' #RSN
# SSID = '1eJOpfJp1AuXybgJeZ3RiAT-b_E0q414V9eXZAppaPf4' #NEW TEST SHEET

def make_connection():
    """Makes a connection to the Google Spreadsheet API. 

    Connects to the Google Sheets API need to create an account in
    Google App Engines and have a key file for credentials. Also need
    to share the sheet with the account asscociated with the key file
    so that it can make edits.

    Returns:
        Authorization to connect and make edits to google spreadsheet.
    """
    scopes = ['https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Clash Rosters-4b34788e38c3.json', scopes)
    return discovery.build('sheets', 'v4', credentials=credentials)


def add_row(SSID, cells, *values):
    """Add rows to the end of the logical table that is located at the cell referenced.

    Arguments:
        SSID (string): Spreadsheet ID of the sheet to be edited.
        cells (string): A1 notation of a cell to search for a logical table.
            Rows will be appended to the end of that table.
        *values (list): Variable length arguments list made up of of lists
            of values to be added to the end of the table.

    Returns:
        {
            "spreadsheetId": string,
            "tableRange": string,
            "updates": {
                        "spreadsheetId": string,
                        "updatedRange": string,
                        "updatedRows": number,
                        "updatedColumns": number,
                        "updatedCells": number,
                        "updatedData": {
                                        "range": string,
                                        "majorDimension": enum(Dimension),
                                        "values": [
                                                   array
                                                   ],

                        }
            },
        }
    """
    service = make_connection()
    value_input_option = 'USER_ENTERED' #TODO: Add this to arguments
    insert_data_option = 'INSERT_ROWS' #TODO: Add this to arguments
    value_range_body = {
      "values": [value for value in values]
    }
    request = service.spreadsheets().values().append(spreadsheetId=SSID,
                                                     range=cells,
                                                     valueInputOption=value_input_option,
                                                     insertDataOption=insert_data_option,
                                                     body=value_range_body)
    response = request.execute()
    return response


def update_cell_values(SSID, cells, values):
    """Add rows to the end of the logical table that is located at the cell referenced.

    Arguments:
        SSID (string): Spreadsheet ID of the sheet to be edited.
        cells (string): A1 notation of a range to update.
        *values (list): Variable length arguments list made up of of lists
            of values to be entered into the cells.

    Returns:
        {
            "spreadsheetId": string,
            "tableRange": string,
            "updates": {
                        "spreadsheetId": string,
                        "updatedRange": string,
                        "updatedRows": number,
                        "updatedColumns": number,
                        "updatedCells": number,
                        "updatedData": {
                                        "range": string,
                                        "majorDimension": enum(Dimension),
                                        "values": [
                                                   array
                                                   ],

                        }
            },
        }
    """
    service = make_connection()
    value_input_option = 'USER_ENTERED'  # TODO: Add this to arguments.
    value_range_body = {
        "values": values
    }
    request = service.spreadsheets().values().update(spreadsheetId=SSID,
                                                     range=cells,
                                                     valueInputOption=value_input_option,
                                                     body=value_range_body)
    response = request.execute()
    return response


def create_data_dict(values, cells, major_dimension="ROWS"):
    """Create a dictionary for use in batch_update_cell_values

    Arguments:
        values (list): List of values to be written.
        cells (string): A1 notation of cell where data should start being written.
        majorDimension (String, optional): Specifies whether each list is a Row or column,
            then splits the data in the list accross the other dimension.
            should be: ROWS/COLUMNS/DIMENSION_UNSPECIFIED.
            Defaults to ROWS.

    Returns:
        dict: dictionary formatted for use in batch_update_cell_values.
    """
    return {"majorDimension": major_dimension,
            "range": cells,
            "values": values
            }


def batch_update_cell_values(SSID, value_input_option, *data):
    """Update a variable number of ranges of cell values.

    Arguments:
        SSID (string): Spreadsheet ID of the sheet to be edited.
        Value_input_option (string): How the values should be handled.
            "INPUT_VALUE_OPTION_UNSPECIFIED", "RAW", "USER_ENTERED"
        *data (dictionary): variable number of data dictionaries created by create_data_dict.

    Returns:
        One instance of the object in per instance of data in the order found in data.
        {
            spreadsheetId": string,
            "updatedRange": string,
            "updatedRows": number,
            "updatedColumns": number,
            "updatedCells": number,
            "updatedData": {
                            "range": string,
                            "majorDimension": enum(Dimension),
                            "values": [
                                        array
                                    ],

                        }
            }
    """
    service = make_connection()
    batch_update_values_request_body = {
                                    'value_input_option': value_input_option, # How the input data should be interpreted.
                                    'data': [info for info in data],  # The new values to apply to the spreadsheet.
                                    }

    request = service.spreadsheets().values().batchUpdate(spreadsheetId=SSID, body=batch_update_values_request_body)
    response = request.execute()
    return response

def get_cells(SSID, cells, major = "ROWS", value_render_option = "FORMATTED_VALUE", date_time_render_option = 'FORMATTED_STRING'):
    """Get the data in the cells for the given range.Get

    Arguments:
        SSID (string): Spreadsheet ID of the sheet to be edited.
        cells (string): A1 notation of range of cells to get values from.
        major (string, optional): The major dimension the results should use. 
            Rows, columns, dimension_undefinied.
            Rows makes a new list for each row with column values inside.
            Columns makes a new list for each column with row values inside.
            Defaults to ROWS.
        value_render_option (string, optional): Determines how values should be rendered in the output.
            "FORMATTED_VALUE": Values will be calculated & formatted in the reply according to the cell's formatting.
            "UNFORMATTED_VALUE": Values will be calculated, but not formatted in the reply.
            "FORMULA": Values will not be calculated.
            Defaults to FORMATTED_VALUE.
        date_time_render_option (string, optional): Determines how dates should be rendered in the output.
            "SERIAL_NUMBER": Number before decimal is days since 12/30/1899, after is time as fraction of the day.
            "FORMATTED_STRING":Instructs date, time, datetime, and duration fields to be output as strings in their 
                given number format. Based on SS Locale.
            Default to FORMATTED_STRING.    
    
    Returns:
        {
         "range": string,
         "majorDimension": enum(Dimension),
         "values": [
                    array: list of values for each row/column in range.
                   ],
        }
    """
    service = make_connection()
    request = service.spreadsheets().values().get(spreadsheetId=SSID,
                                                  range=cells, 
                                                  valueRenderOption=value_render_option, 
                                                  majorDimension = major, 
                                                  dateTimeRenderOption=date_time_render_option)
    response = request.execute()
    return response

def get_spreadsheet(SSID, include_grid_data = False, *ranges):
    """Return the spreadsheet at the given ID.
    
    Arguments:
        SSID (string): Spreadsheet ID of the spreadsheet to get.
        include_grid_data (bool, optional): True if grid data should be returned. Default to False
        *ranges (string, optional): Variable length list of strings of the ranges to return from the spreadsheet in A1 format.
        
    Returns:
            {
            "spreadsheetId": string,
            "properties": {
                          "title": string,
                          "locale": string,
                          "autoRecalc": enum(RecalculationInterval), # When values are recalculated 
                          "timeZone": string,
                          "defaultFormat": {
                            "numberFormat": {
                                            object(NumberFormat)
                                          },
                                          "backgroundColor": {
                                            object(Color)
                                          },
                                          "borders": {
                                            object(Borders)
                                          },
                                          "padding": {
                                            object(Padding)
                                          },
                                          "horizontalAlignment": enum(HorizontalAlign),
                                          "verticalAlignment": enum(VerticalAlign),
                                          "wrapStrategy": enum(WrapStrategy),
                                          "textDirection": enum(TextDirection),
                                          "textFormat": {
                                            object(TextFormat)
                                          },
                                          "hyperlinkDisplayType": enum(HyperlinkDisplayType),
                                          "textRotation": {
                                            object(TextRotation)
                                          }, 
                          },
                          "iterativeCalculationSettings": {
                                                            "maxIterations": number,
                                                            "convergenceThreshold": number,
                                                            },
                          },
            "sheets": [
                        {
                          object(Sheet)
                        }
                      ],
            "namedRanges": [
                            {
                              object(NamedRange)
                            }
                           ],
            "spreadsheetUrl": string,
            "developerMetadata": [
                                    {
                                      object(DeveloperMetadata)
                                    }
                                  ],
            }
    """
    service = make_connection()
    _range = [range_ for range_ in ranges]
    request = service.spreadsheets().get(spreadsheetId=SSID, ranges=_range, includeGridData=include_grid_data)
    return request.execute()
    

def clear_range_values(SSID, *ranges):
    """Clears the values of a variable number of ranges.
    
    Arguments: 
        SSID (string): Spreadsheet ID of the spreadsheet to modify.
        *ranges (string): Variable number of ranges in A1 notation to clear.
    
    Returns:
        {
          "spreadsheetId": string,
          "clearedRanges": [
            string #ranges that have been cleared.
          ],
        }
    """
    service = make_connection()
    batch_clear_values_request_body = {
    
    'ranges': [range_ for range_ in ranges], # The ranges to clear, in A1 notation.

    }

    request = service.spreadsheets().values().batchClear(spreadsheetId=SSID, body=batch_clear_values_request_body)

    return request.execute()


#Batch Update Requests

def add_borders(sheet_id, row):
    request ={
         "updateBorders":{
            "range":{
               "sheetId":sheet_id,
               "startColumnIndex":0,
               "startRowIndex":row,
               "endRowIndex":row+1
            },
            "innerVertical":{
               "style":"SOLID_MEDIUM"
            },
            "right":{
               "style":"SOLID_MEDIUM"
            }
         }
      }
    return request

def duplicate_sheet(source, name):
    request = {
         "duplicateSheet":{
            "sourceSheetId":source,
            "newSheetName":name,
            "insertSheetIndex":0
         }
      }
    return request

def merge_cells(sheet_id, row, col, num_of_rows = 1, num_of_cols = 1, style= "MERGE_ALL"):
    request = {
          "mergeCells": {
            "range": {
              "sheetId": sheet_id,
              "startRowIndex": row,
              "endRowIndex": row + num_of_rows,
              "startColumnIndex": col,
              "endColumnIndex": col + num_of_cols
            },
            "mergeType": style
          }
        }
    return request

def sort_range(sheet_id, start_row, start_col, num_of_rows = 1, num_of_cols = 1, sort_col = 1, order = "ASCENDING"):
    """Create a batch update object to sort a range.
    
    Arguments:
        sheet_id (string): The ID number of the sheet within the spreadsheet to sort.
        start_row (int): The 0 based index location of the start row to sort.
        start_col (int): The 0 based index location of the start colunn to sort.
        num_of_rows (int, optional): The number of rows to include in the sort range. Defaults to 1. 
        num_of_cols (int, optional): The number of colunns to include in the sort range. Defaults to 1. 
        sort_col (int, optional): The dimension of the column number that the sort should be applied to. Defaults to 1. 
        order (string, optional): Sort Ascending or Descending. Defaults to Ascending.
    
    Returns: 
        Batch update request object.
    """
    request = {
        "sortRange": {
            "range": {
            "sheetId": sheet_id,
            "startRowIndex": start_row,
            "endRowIndex": start_row + num_of_rows,
            "startColumnIndex": start_col,
            "endColumnIndex": start_col + num_of_cols
            },
            "sortSpecs": [
                {
                "dimensionIndex": sort_col,
                "sortOrder": order
                }
            ]
            }
        }
    return request

def batch_update(SSID, *requests):
    """Apply one or more updates to a spreadsheet.`
    
    Arguments:
        SSID (string): Spreadsheet ID of the spreadsheet to modify.
        *requests (object): Variable number of requests to modify the sheet as created by any batch request function.
        
    Returns:
        {
          "spreadsheetId": string,
          "replies": [
            {
              object(Response)
            }
          ],
        }
    """
    service = make_connection()
    batch_update_spreadsheet_request_body = {"requests": [request for request in requests]}
    request = service.spreadsheets().batchUpdate(spreadsheetId=SSID, body=batch_update_spreadsheet_request_body)
    return request.execute()



if __name__ == "__main__":
    print(get_spreadsheet()["sheets"][0]["properties"]["sheetId"])
