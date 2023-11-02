import datetime
import traceback
from typing import Tuple
from scraper import Scraper


class C:

    def __init__(self, scraper: Scraper) -> None:
        self.scraper = scraper

    def get_rows(self) -> list:
        return self.scraper.xPath(path='//table[@id="tablematch1"]/tbody/tr')

    def extract_data(self, parser: Scraper, type: str) -> None:
        odds = []

        self.scraper.click(path='//a[@class="_agreement"]')

        while True:

            try:
                self.scraper.freeze()

                all_rows = self.get_rows()

                for i in range(0, int(len(all_rows) / 5)):
                    rows = all_rows[0:5]
                    all_rows.pop(0)
                    all_rows.pop(1)
                    all_rows.pop(2)
                    all_rows.pop(3)
                    all_rows.pop(4)

                    championship_name = self.scrape_championship(info=rows[0])
                    match_status, yellow_cards_home, red_cards_home, team_home, minute_in_progress, date_time, ft_home, ht, odds_out_1, odds_out_x, odds_out_2, odds_in_1, odds_in_x, odds_in_2 = self.scrape_team_home(info=rows[1])
                    yellow_cards_away, red_cards_away, team_away, ft_away, ck = self.scrape_team_away(info=rows[2])
                    spread_cu_home, spread_op_home, odds_cu_home, odds_op_home, totalline_cu, totalline_op, overunder_r_home, overunder_cu_home, overunder_op_home, ptpay_val_home, ptpay_uo_home, tot, euroodds_1_home, euroodds_x_home, euroodds_2_home, gol25_ov_home, gol25_un_home, ggng_yes_home, ggng_no_home, mg14_yes_home, mg14_no_home, tips = self.scrape_team_home_statistics(stat=rows[3])
                    spread_cu_away, spread_op_away, odds_cu_away, odds_op_away, overunder_r_away, overunder_cu_away, overunder_op_away, ptpay_val_away, ptpay_uo_away, euroodds_1_away, euroodds_x_away, euroodds_2_away, gol25_ov_away, gol25_un_away, ggng_yes_away, ggng_no_away, mg14_yes_away, mg14_no_away = self.scrape_team_away_statistics(stat=rows[4])

            except Exception as e:
                print(f'Error while scraping: {e}')
                print('Stacktrace: ' + traceback.format_exc())
            finally:
                self.scraper.unfreeze()

    def scrape_championship(self, info: any) -> str:
        return self.scraper.xPath(element=info, path='.//td[1]', prop='text()').encode('utf-8')

    def scrape_team_home(self, info: any) -> Tuple[str, int, int, str, int, datetime.datetime, int, str, float, float, float, float, float, float]:
        yellow_cards_home = self.scraper.xPath(element=info, path='.//td[@class="name"]/span[@class="yellowcard"]', prop='text()')
        red_cards_home = self.scraper.xPath(element=info, path='.//td[@class="name"]/span[@class="redcard"]', prop='text()')
        team_home = self.get_team(element=info, yellow_cards=yellow_cards_home, red_cards=red_cards_home)

        date_time, minute_in_progress, match_status = self.get_minute(info=info)

        ft_home = self.scraper.xPath(element=info, path='.//td[4]', prop='text()')
        ht = self.scraper.xPath(element=info, path='.//td[6]', prop='text()')

        # out
        odds_out_1 = self.scraper.xPath(element=info, dataType='NUMBER', path='.//td[8]', prop='text()', explode='"\n", 0')
        odds_out_x = self.scraper.xPath(element=info, dataType='NUMBER', path='.//td[8]', prop='text()', explode='"\n", 1')
        odds_out_2 = self.scraper.xPath(element=info, dataType='NUMBER', path='.//td[8]', prop='text()', explode='"\n", 2')

        # in
        odds_in_1 = self.scraper.xPath(element=info, dataType='NUMBER', path='.//td[9]', prop='text()', explode='"\n", 0')
        odds_in_x = self.scraper.xPath(element=info, dataType='NUMBER', path='.//td[9]', prop='text()', explode='"\n", 1')
        odds_in_2 = self.scraper.xPath(element=info, dataType='NUMBER', path='.//td[9]', prop='text()', explode='"\n", 2')

        return match_status, yellow_cards_home, red_cards_home, team_home, minute_in_progress, date_time, ft_home, ht, odds_out_1, odds_out_x, odds_out_2, odds_in_1, odds_in_x, odds_in_2

    def scrape_team_away(self, info: any) -> Tuple[int, int, str, int, int]:
        yellow_cards_away = self.scraper.xPath(element=info, path='.//td[@class="name"]/span[@class="yellowcard"]', prop='text()')
        red_cards_away = self.scraper.xPath(element=info, path='.//td[@class="name"]/span[@class="redcard"]', prop='text()')
        team_away = self.get_team(element=info, yellow_cards=yellow_cards_away, red_cards=red_cards_away)
        ft_away = self.scraper.xPath(element=info, path='.//td[3]', prop='text()')
        ck = self.scraper.xPath(element=info, path='.//td[5]', prop='text()')

        return yellow_cards_away, red_cards_away, team_away, ft_away, ck

    def scrape_team_home_statistics(self, stat: any) -> Tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]:
        spread_cu_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[2]', prop='text()')
        spread_op_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[3]', prop='text()')
        odds_cu_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[5]', prop='text()')
        odds_op_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[6]', prop='text()')
        totalline_cu = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[7]', prop='text()')
        totalline_op = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[8]', prop='text()')
        overunder_r_home = self.scraper.xPath(element=stat, path='.//td[9]', prop='text()')
        overunder_cu_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[11]', prop='text()')
        overunder_op_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[12]', prop='text()')
        ptpay_val_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[13]', prop='text()')
        ptpay_uo_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[14]', prop='text()')
        tot = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[15]', prop='text()')
        euroodds_1_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[16]', prop='text()')
        euroodds_x_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[17]', prop='text()')
        euroodds_2_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[18]', prop='text()')
        gol_25_ov_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[19]', prop='text()')
        gol_25_un_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[20]', prop='text()')
        ggng_yes_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[21]', prop='text()')
        ggng_no_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[22]', prop='text()')
        mg14_yes_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[23]', prop='text()')
        mg14_no_home = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[24]', prop='text()')
        tips = self.scraper.xPath(element=stat, path='.//td[25]', prop='html()', replace='"<br>"; ", "')

        return spread_cu_home, spread_op_home, odds_cu_home, odds_op_home, totalline_cu, totalline_op, overunder_r_home, overunder_cu_home, overunder_op_home, ptpay_val_home, ptpay_uo_home, tot, euroodds_1_home, euroodds_x_home, euroodds_2_home, gol_25_ov_home, gol_25_un_home, ggng_yes_home, ggng_no_home, mg14_yes_home, mg14_no_home, tips

    def scrape_team_away_statistics(self, stat: any) -> Tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]:
        spread_cu_away = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[2]', prop='text()')
        spread_op_away = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[3]', prop='text()')
        odds_cu_away = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[5]', prop='text()')
        odds_op_away = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[6]', prop='text()')
        overunder_r_away = self.scraper.xPath(element=stat, path='.//td[7]', prop='text()')
        overunder_cu_away = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[9]', prop='text()')
        overunder_op_away = self.scraper.xPath(element=stat, dataType='NUMBER', path='.//td[10]', prop='text()')
        ptpay_val_away = self.scraper.xPath(element=stat, dataType='PERCENTAGE', path='.//td[11]', prop='text()')
        ptpay_uo_away = self.scraper.xPath(element=stat, dataType='PERCENTAGE', path='.//td[12]', prop='text()')
        euroodds_1_away = self.scraper.xPath(element=stat, dataType='PERCENTAGE', path='.//td[13]', prop='text()')
        euroodds_x_away = self.scraper.xPath(element=stat, dataType='PERCENTAGE', path='.//td[14]', prop='text()')
        euroodds_2_away = self.scraper.xPath(element=stat, dataType='PERCENTAGE', path='.//td[15]', prop='text()')
        gol25_ov_away = self.scraper.xPath(element=stat, dataType='PERCENTAGE', path='.//td[16]', prop='text()')
        gol25_un_away = self.scraper.xPath(element=stat, dataType='PERCENTAGE', path='.//td[17]', prop='text()')
        ggng_yes_away = self.scraper.xPath(element=stat, dataType='PERCENTAGE', path='.//td[18]', prop='text()')
        ggng_no_away = self.scraper.xPath(element=stat, dataType='PERCENTAGE', path='.//td[19]', prop='text()')
        mg14_yes_away = self.scraper.xPath(element=stat, dataType='PERCENTAGE', path='.//td[20]', prop='text()')
        mg14_no_away = self.scraper.xPath(element=stat, dataType='PERCENTAGE', path='.//td[21]', prop='text()')

        return spread_cu_away, spread_op_away, odds_cu_away, odds_op_away, overunder_r_away, overunder_cu_away, overunder_op_away, ptpay_val_away, ptpay_uo_away, euroodds_1_away, euroodds_x_away, euroodds_2_away, gol25_ov_away, gol25_un_away, ggng_yes_away, ggng_no_away, mg14_yes_away, mg14_no_away

    def get_minute(self, info: any) -> Tuple[datetime.datetime, int, str]:
        minute_in_progress = self.scraper.xPath(element=info, path='.//td[3]', prop='text()')
        if minute_in_progress is not None:
            if ':' in minute_in_progress:
                # reset minute_in_progress
                minute_in_progress = None

                # the match is over and it is reported with it starting date and time
                match_status = MatchModes.PAST
                date = self.scraper.xPath(element=info, path='.//td[3]', prop='text()', explode='"\n", 0')
                year = datetime.datetime.now().year - 1 if date == '31-12' else datetime.datetime.now().year
                time = self.scraper.xPath(element=info, path='.//td[3]', prop='text()', explode='"\n", 1')
                date_time = datetime.datetime.strptime(f'{date}-{year} {time}', '%d-%m-%Y %H:%M')
            else:
                # the match is in progress. Its starting time needs to be calculated as now() - minute_in_progress
                # the result needs to be rounded by 15 minutes because minute_in_progress is not constantly updated
                match_status = MatchModes.LIVE
                if minute_in_progress == MatchEvents.HALFTIME:
                    minute_in_progress = 45
                elif minute_in_progress == MatchEvents.OVERTIME:
                    minute_in_progress = 90
                elif minute_in_progress == MatchEvents.PENALTIES:
                    minute_in_progress = 120
                else:
                    try:
                        minute_in_progress = int(minute_in_progress.replace("'", "").replace("+", "")) # half time = 45 minutes
                    except Exception as e:
                        minute_in_progress = 90

                date_time = datetime.datetime.now() - datetime.timedelta(minutes=minute_in_progress)
                date_time = date_time - datetime.timedelta(minutes=date_time.minute % 15, seconds=date_time.second, microseconds=date_time.microsecond)

        return date_time, minute_in_progress, match_status

    def get_team(self, element: any, yellow_cards: int, red_cards: int) -> str:
        team = self.scraper.xPath(element=element, path='.//td[@class="name"]', prop='text()')
        team = team[len(yellow_cards):] if yellow_cards is not None and team is not None else team
        team = team[len(red_cards):] if red_cards is not None and team is not None else team
        team = team.encode('utf-8')

        return team

class MatchModes:
    LIVE = 'LIVE'
    PAST = 'PAST'

class MatchEvents:
    HALFTIME = 'HT'
    OVERTIME = 'OT'
    PENALTIES = 'PEN'