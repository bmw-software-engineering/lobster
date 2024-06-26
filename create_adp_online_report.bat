rem This script runs LOBSTER on windows. its genrates the HTML report.
rem python lobster\tools\cpp_parser\cpp_parser.py  C:\Projects\BMW\adp --out adp.lobster
lobster-report --lobster-config="lobster_adp_report.config" --out="report.lobster"
lobster-html-report report.lobster --out="lobster_adp_online_report.html"
