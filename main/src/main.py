from authentication import Authentication 
from technical_analysis import TechnicalAnalysis    
from report import ReportGenerator    
def main():
    """Main function to run the portfolio tracker"""
    print("Wealthsimple Portfolio Tracker with Performance Analysis")
    print("------------------------------------------------------")
    auth, tech_analysis, report = Authentication(), TechnicalAnalysis(), ReportGenerator()
    print("Getting holdings, analyzing performance and generating report...")
    report_file = report.generate_report(analysis_results = tech_analysis.analyze_performance(auth.get_holdings()))
    
    print(f"Complete! Report generated: {report_file}")

if __name__ == "__main__":
    main()