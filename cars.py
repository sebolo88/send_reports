#!/usr/bin/env python3

import json
import locale
import sys
import reports
import emails

def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
  return data


def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(
      car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
  """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
  max_revenue = {"revenue": 0}
  max_sales = {"sales":0}
  best_year = 0
  sales = 0
  car_year = {}
  for item in data:
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item
    # TODO: also handle max sales
    if item["total_sales"] > sales:
      max_sales = item
    # TODO: also handle most popular car_year
    if car_year.get(item['car']['car_year'])==None:
      car_year[item['car']['car_year']]=item['total_sales']
    else:
      car_year[item['car']['car_year']]+=item['total_sales']
    sales=0
    for year in car_year:
      if  car_year[year]>sales:
        sales=car_year[year]
        best_year = year
  summary = [
    "The {} generated the most revenue: ${}".format(
      format_car(max_revenue["car"]), max_revenue["revenue"]),
  ]
  summary.append("The {} had the most sales: {}".format(format_car(max_sales["car"]),max_sales["total_sales"]))
  summary.append("The most popular year was {} with {} sales.".format(best_year, sales))
  return summary


def cars_dict_to_table(car_data):
  """Turns the data in car_data into a list of lists."""
  table_data = [["ID", "Car", "Price", "Total Sales"]]
  for item in car_data:
    table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
  return table_data


def main(argv):
  """Process the JSON data and generate a full report out of it."""
  data = load_data("car_sales.json")
  summary = process_data(data)
  print(summary)
  cars_list=cars_dict_to_table(data)
  reports.generate('/tmp/cars.pdf','Raport',"<br/>".join(summary), cars_list)
  message = emails.generate('automation@example.com', 'student-04-c86cd7407444@example.com', 'Sales summary for last month', '\n'.join(summary),'/tmp/cars.pdf')
  emails.send(message)
if __name__ == "__main__":
  main(sys.argv)





