""" SFOS Ground Control
Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License.You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed
to in writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See
the License for the specific language governing permissions and limitations under the
License.
"""

from dataclasses import dataclass
import pandas as pd


@dataclass
class PageData:
    """response class for _fetchdata call"""

    all_rows: pd.DataFrame
    page_size: int = 0
    row_count: int = -1
    current_page: int = 0
    page_count: int = -1
    page_start: int = -1
    page_end: int = -1

    def __init__(
        self,
        data: pd.DataFrame,
        page_size: int = 25,
        current_page: int = 0,
    ):
        """Paginate a Pandas DataFrame

        Args:
            all_data (pd.DataFrame): Data to be paginated
            current_page (int, optional): page of data to select.
                                          First page is 0
                                          Defaults to 0.
            page_size (int, optional): Records per page.
                                       0 = Do not paginate
                                       Defaults to 0.
        """
        # set dataframe vars
        self.all_rows = data
        self.row_count = len(data)

        # Define remaining variables with placeholder values
        self.page_size: int = page_size  # Updated by self.set_page()
        self.page_count: int = -1
        self.page_start: int = -1  # Existence req'd by self.set_page_size()
        #                            Updated by self.set_page()
        self.current_page: int = current_page
        self.page_end: int = current_page  # Updated by self.set_page()

        # Now count how many pages and set the current page
        self.set_page_size(rows_per_page=page_size)
        self.set_page(page_no=current_page)

    def set_page_size(self, rows_per_page: int):
        """Set the pagination page size and page count

        Args:
            rows_per_page (int | None): Number of rows on a page
        """

        firstrow = self.page_start or 0
        if self.page_start >= 0:
            firstrow = self.page_start

        if rows_per_page > 0:  # Paginate
            full_pages, remaining_rows = divmod(self.row_count, rows_per_page)
            self.page_count = full_pages + (1 if remaining_rows else 0)
        else:  # Don't paginate
            self.page_size = 0
            self.page_count = 1  # data not paginated

        if firstrow >= 0:  # make sure the first row on the page is on new current page
            self.set_page(row_no=firstrow)

        print(
            f"set_page_size='{self.page_size}' "
            f"page_count={self.page_count}. "
            f"page={self.current_page}"
        )

    def set_page(self, page_no: int | None = None, row_no: int | None = None):
        """Calculate the currnet page window from the current page number
        or supplied arguments"""
        print(f"setting page to ({page_no}) or row {row_no}")
        # Does the data need to be paginated?
        if not self.page_size or self.page_size == 0 or self.page_count == 1:
            self.page_size = 0
            self.current_page = 0
            self.page_start = 0
            self.page_end = self.row_count
        else:
            # was a valid row_no provided?
            if row_no and row_no < self.row_count:
                # find the row's page number
                page_no = divmod(row_no, self.page_size)[0]

            # is a valid page number provided?
            if page_no and page_no < self.page_count:
                self.current_page = page_no

            # Is current_page set?
            if not self.current_page:
                self.current_page = 0

            # By now: page_size, current_page should definitely be set
            # Find the first and last records on the last page
            self.page_start = self.current_page * self.page_size

            if self.page_size >= self.row_count:
                self.page_end = self.row_count
            else:
                self.page_end = self.page_start + self.page_size - 1
        print(f"result: {self.current_page}")

    def next_page(self) -> pd.DataFrame:
        """Move to the next page if this isn't already the last page"""
        if self.current_page < (self.page_count - 1):
            self.set_page(page_no=self.current_page + 1)
        return self.page_rows()

    def prev_page(self) -> pd.DataFrame:
        """Move to the prev page if this isn't already the first page"""
        if self.current_page > 0:
            self.set_page(page_no=self.current_page - 1)
        return self.page_rows()

    def first_page(self) -> pd.DataFrame:
        """Move to the first page of data"""
        self.set_page(page_no=0)
        return self.page_rows()

    def last_page(self) -> pd.DataFrame:
        """Move to the last page of data"""
        self.set_page(page_no=self.page_count - 1)
        return self.page_rows()

    def current_page_rows(self) -> pd.DataFrame:
        """Data on the current page"""
        return self.page_rows()

    def page_rows(self, page_number: int | None = None) -> pd.DataFrame:
        """Grabs the current page of row data from all_rows"""
        if page_number != self.current_page:
            self.set_page((page_number))
        print(
            f"returning rows from {self.page_start} to {self.page_end} - page_size={self.page_size}"
        )
        return self.all_rows[self.page_start : self.page_end]
