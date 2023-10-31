import os
import pygsheets
import pandas as pd
from pygsheets import DataRange


class Gsheets:
    """
    Pass in a service account file path and query data stored in Google Sheets
    Example: Gsheets('SPREADSHEET').query('WORKSHEET')
    """

    def __init__(self, spreadsheet):
        self.client = pygsheets.authorize(
            service_account_env_var="GOOGLE_SHEETS_CREDENTIALS")
        self.spreadsheet_key = os.getenv(spreadsheet)
        self.spreadsheet = self.client.open_by_key(self.spreadsheet_key)

    def query(self, worksheet, start_cell=None, end_cell=None):
        """
        Returns results of spreadsheet, worksheet as a pandas DataFrame
        Spreadsheet is stored as env var
        Worksheet is passed in as plain text
        """
        ws = self.spreadsheet.worksheet_by_title(worksheet)
        df = ws.get_as_df(start=start_cell, end=end_cell)
        print(
            f"{self.spreadsheet.title}.{worksheet}: Downloaded {df.shape} shape"
        )
        return df

    # If get_as_df does not work, use this instead
    def select_all_values(self, worksheet):
        return pd.DataFrame(
            self.spreadsheet.worksheet_by_title(worksheet).get_all_records())

    def write_df(self, df, worksheet, start_cell='A1'):
        self.spreadsheet.worksheet_by_title(worksheet).set_dataframe(
            df, start=start_cell)

    def write_df_with_timestamp(self, df, worksheet):
        # Create worksheet if not exists
        try:
            worksheet = self.spreadsheet.worksheet_by_title(worksheet)
        except Exception as e:
            worksheet = self.spreadsheet.add_worksheet(title=worksheet)

        # Add a timestamp to the df
        df['updated_at'] = pd.Timestamp("now")

        # Clear existing data
        worksheet.clear(start='A1')

        # Write the frame to the worksheet, adding rows if necessary
        worksheet.set_dataframe(df, start="A1", extend=True)

        NUM_ROWS = df.shape[0] + 1
        NUM_COLS = df.shape[1]

        # Resize the worksheet to the shape of the frame
        worksheet.resize(rows=NUM_ROWS, cols=NUM_COLS)

        # Create the DataRange object
        drange = DataRange(start='A1', worksheet=worksheet)

        # Add borders to the DataRange
        drange.update_borders(top=True,
                              right=True,
                              bottom=True,
                              left=True,
                              inner_horizontal=True,
                              inner_vertical=True,
                              style='SOLID')

        # Complete message
        print(
            f"Wrote {len(df)} rows to {self.spreadsheet.title}.{worksheet.title}"
        )