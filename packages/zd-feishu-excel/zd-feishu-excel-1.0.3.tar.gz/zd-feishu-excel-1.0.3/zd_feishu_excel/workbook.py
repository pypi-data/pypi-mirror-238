import requests
from .utils import must
from .cell import Cell, get_column_letter, get_cell_letter
import logging


class Sheet(object):
    def __init__(self, app, ss_token, sheet_info):
        self._app = app
        self._ss_token = ss_token
        self.sheet_info = sheet_info
        self.data = self.get_sheet_from_remote()
        self.cells = self.convert_data_to_cell(self.data)
        self.changes = dict()

    def __str__(self):
        return str(self.data)

    @staticmethod
    def convert_data_to_cell(data):
        cells = dict()
        for i in range(len(data)):
            for j in range(len(data[i])):
                row = i + 1
                column = j + 1
                value = data[i][j]
                cell = Cell(row=row, column=column, value=value)
                cells[get_cell_letter(row, column)] = cell
        return cells

    def cell(self, row, col, value=None):
        """读、写"""
        assert row > 0 and col > 0
        cell_letter = get_cell_letter(row, col)
        if value is None:
            c = self.cells.get(cell_letter)
            if isinstance(c, Cell):
                return c.value
            else:
                return c
        else:
            range_text = '{}:{}'.format(cell_letter, cell_letter)
            self.changes[range_text] = [[value]]
            self.cells[cell_letter] = value
            return value

    def save(self):
        if len(self.changes) == 0:
            logging.debug("not changes detected, ignore save")
            return
        self.batch_set_range(self.changes)
        self.data = self.get_sheet_from_remote()
        self.cells = self.convert_data_to_cell(self.data)
        self.changes = dict()

    @property
    def max_row(self):
        return len(self.data)

    def all_range(self, start='A1'):
        sheet_info = self.sheet_info
        return '{}!{}:{}{}'.format(
            sheet_info['sheetId'],
            start,
            row_key(sheet_info['rowCount']),
            sheet_info['columnCount'],
        )

    def get_range(self, rangeText, render_opt='FormattedValue', no_nils=True):
        url = ('https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/'
               '{}/values/{}?valueRenderOption={}') \
            .format(self._ss_token, rangeText, render_opt)
        logging.debug(url)
        r = must(requests.get(url, headers=dict(
            Authorization='Bearer ' + self._app.get_tenant_access_token(),
        )))
        data = r['valueRange']['values']
        if no_nils:
            data = remove_nils(data)
        return data

    def get_sheet_from_remote(self, start='A1', render_opt='FormattedValue', no_nils=True):
        return self.get_range(self.all_range(start), render_opt, no_nils)

    def batch_set_range(self, changes):
        url = 'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{}/values_batch_update'.format(self._ss_token)
        headers = {
            'Authorization': 'Bearer ' + self._app.get_tenant_access_token(),
            'Content-Type': 'application/json; charset=utf-8'
        }
        data_change = []
        for r in changes:
            range_text = '{}!{}'.format(self.sheet_info['sheetId'], r)
            data_change.append({"range": range_text, "values": changes[r]})
        data = {'valueRanges': data_change}

        rsp = requests.post(url, headers=headers, json=data)
        r = must(rsp)
        return r

    def __getitem__(self, key):
        """Returns a cell value by its key.

        :param name: the name of the worksheet to look for
        :type name: string

        """
        if key in self.cells:
            return self.cells[key].value
        else:
            return None


class Workbook(object):
    def __init__(self, ss_token, app=None):
        self._app = app
        self._ss_token = ss_token
        self._meta = None

        self.sheets = dict()

    def get_meta(self):
        return self._meta if self._meta is not None else self.refresh_meta()

    def refresh_meta(self):
        url = 'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{}/metainfo'.format(self._ss_token)
        logging.debug(url)
        self._meta = must(requests.get(url, headers=dict(
            Authorization='Bearer ' + self._app.get_tenant_access_token(),
        )))
        return self._meta

    def sheet_info(self, sheet_key):
        sheet_info = None
        if isinstance(sheet_key, int):
            sheet_info = self.get_meta()['sheets'][sheet_key]
        elif isinstance(sheet_key, str):
            for s in self.get_meta()['sheets']:
                if s['title'] == sheet_key:
                    sheet_info = s
                    break
        if sheet_info is None:
            raise Exception('can not find sheet id for key {}'.format(sheet_info))
        return sheet_info

    def sheet_id(self, sheet_key):
        return self.sheet_info(sheet_key)['sheetId']

    def make_range(self, row1, col1, row2, col2):
        pass

    def all_range(self, sheet_info, start='A1'):
        return '{}!{}:{}{}'.format(
            sheet_info['sheetId'],
            start,
            row_key(sheet_info['rowCount']),
            sheet_info['columnCount'],
        )

    def get_range(self, rangeText, render_opt='FormattedValue', no_nils=True):
        url = ('https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/'
               '{}/values/{}?valueRenderOption={}') \
            .format(self._ss_token, rangeText, render_opt)
        logging.debug(url)
        r = must(requests.get(url, headers=dict(
            Authorization='Bearer ' + self._app.get_tenant_access_token(),
        )))
        data = r['valueRange']['values']
        if no_nils:
            data = remove_nils(data)
        return data

    def get_sheet(self, sheet_key, start='A1', render_opt='FormattedValue', no_nils=True):
        return self.get_range(self.all_range(self.sheet_info(sheet_key), start), render_opt, no_nils)

    def create_sheet(self, sheet_name):
        url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{}/sheets_batch_update" \
            .format(self._ss_token)
        headers = {
            'Authorization': 'Bearer ' + self._app.get_tenant_access_token(),
            'Content-Type': 'application/json; charset=utf-8'
        }
        body = {"requests": [
            {"addSheet": {"properties": {"title": sheet_name}}}
        ]}

        rsp = requests.post(url, headers=headers, json=body)
        r = must(rsp)
        self.refresh_meta()
        return r

    def __getitem__(self, key):
        """Returns a worksheet by its name.

        :param name: the name of the worksheet to look for
        :type name: string

        """
        if key not in self.sheets:
            for s in self.get_meta()['sheets']:
                if s['title'] == key:
                    self.sheets[key] = Sheet(self._app, self._ss_token, s)
                    break

        if key not in self.sheets:
            raise KeyError("Worksheet {0} does not exist.".format(key))
        return self.sheets[key]

    def __iter__(self):
        return iter(self.sheets)

    def __contains__(self, item):
        for s in self.get_meta()['sheets']:
            if s['title'] == item:
                return True
        return False


def row_key(index):
    s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    assert index > 0
    res = ''
    while index > 0:
        index -= 1
        p = index % 26
        res = s[p] + res
        index //= 26
    return res


def remove_nil_rows(data):
    n = len(data)
    while n > 0:
        last = n - 1
        has_data = False
        for item in data[last]:
            if item is not None:
                has_data = True
                break
        if has_data:
            break
        n = last
    return data[:n]


def remove_nil_cols(data):
    max_cols = 0
    for row in data:
        cols = len(row)
        while cols > 0:
            p = cols - 1
            if row[p] is None:
                cols = p
            else:
                break
        if cols > max_cols:
            max_cols = cols
    return [row[:max_cols] for row in data]


def remove_nils(data):
    return remove_nil_cols(remove_nil_rows(data))
