from logger import Logger

from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.logger = Logger("ReportGenerator")
        pass
    def generate_report(self, output_file='portfolio_report.html', analysis_results={}):
        """Generate an HTML report of the portfolio analysis"""
        if not analysis_results:
            self.logger.warning("No analysis results available. Run analyze_performance() first.")
            return
            
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Wealthsimple Portfolio Analysis Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1, h2, h3 { color: #333; }
                .account { margin-bottom: 30px; border: 1px solid #ddd; padding: 15px; border-radius: 5px; }
                .position { margin-bottom: 20px; padding: 10px; background-color: #f9f9f9; border-radius: 5px; }
                .buy { color: green; font-weight: bold; }
                .sell { color: red; font-weight: bold; }
                .hold { color: #f39c12; font-weight: bold; }
                .metrics { display: flex; flex-wrap: wrap; }
                .metric { margin: 10px; padding: 10px; border: 1px solid #eee; border-radius: 5px; width: 200px; }
                table { border-collapse: collapse; width: 100%; margin-top: 10px; }
                table, th, td { border: 1px solid #ddd; }
                th, td { padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Wealthsimple Portfolio Analysis Report</h1>
            <p>Generated on: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        """
        
        # Add account sections
        for account_type, positions in analysis_results.items():
            html_content += f"""
            <div class="account">
                <h2>{account_type} Account</h2>
                <p>Number of positions: {len(positions)}</p>
            """
            
            # Add position sections
            for symbol, analysis in positions.items():
                position_data = analysis['position_data']
                technical = analysis['technical_analysis']
                research = analysis['research_analysis']
                summary = analysis['summary']
                
                # Determine the CSS class for the recommendation
                rec_class = 'hold'
                if 'BUY' in summary['overall_recommendation']:
                    rec_class = 'buy'
                elif 'SELL' in summary['overall_recommendation']:
                    rec_class = 'sell'
                
                # Position header
                company_name = position_data.get('stock', {}).get('name', symbol)
                quantity = position_data.get('quantity', 'N/A')
                price = position_data.get('quote', {}).get('amount', 'N/A')
                market_value = position_data.get('market_value', {}).get('amount', 'N/A')
                
                html_content += f"""
                <div class="position">
                    <h3>{symbol} - {company_name}</h3>
                    <p>Quantity: {quantity} | Current Price: ${price} | Market Value: ${market_value}</p>
                    <p>Recommendation: <span class="{rec_class}">{summary['overall_recommendation']}</span></p>
                    
                    <h4>Performance Summary</h4>
                    <ul>
                """
                
                # Add key points
                for point in summary['key_points']:
                    html_content += f"<li>{point}</li>\n"
                
                html_content += "</ul>\n"
                
                # Add technical metrics section
                html_content += """
                    <h4>Technical Metrics</h4>
                    <div class="metrics">
                """
                
                if 'error' not in technical:
                    # SMA
                    if 'sma' in technical:
                        html_content += f"""
                        <div class="metric">
                            <h5>Moving Averages</h5>
                            <p>Current Price: ${technical['sma']['price']:.2f}</p>
                            <p>SMA 20: ${technical['sma']['sma20']:.2f}</p>
                            <p>SMA 50: ${technical['sma']['sma50']:.2f}</p>
                            <p>SMA 200: ${technical['sma']['sma200']:.2f}</p>
                            <p>Trend: {technical['sma']['sma_trend']}</p>
                        </div>
                        """
                    
                    # RSI
                    if 'rsi' in technical:
                        html_content += f"""
                        <div class="metric">
                            <h5>RSI (14-day)</h5>
                            <p>Value: {technical['rsi']['value']:.2f}</p>
                            <p>Signal: {technical['rsi']['signal']}</p>
                        </div>
                        """
                    
                    # MACD
                    if 'macd' in technical:
                        html_content += f"""
                        <div class="metric">
                            <h5>MACD</h5>
                            <p>MACD Line: {technical['macd']['macd_line']:.4f}</p>
                            <p>Signal Line: {technical['macd']['signal_line']:.4f}</p>
                            <p>Histogram: {technical['macd']['histogram']:.4f}</p>
                            <p>Signal: {technical['macd']['signal']}</p>
                        </div>
                        """
                    
                    # Performance
                    if 'performance' in technical:
                        html_content += f"""
                        <div class="metric">
                            <h5>Historical Performance</h5>
                            <p>Period: {technical['performance']['start_date']} to {technical['performance']['end_date']}</p>
                            <p>Change: {technical['performance']['percent_change']:.2f}%</p>
                        </div>
                        """
                else:
                    html_content += f"""
                    <div class="metric">
                        <h5>Technical Analysis Error</h5>
                        <p>{technical['error']}</p>
                    </div>
                    """
                
                html_content += "</div>\n"  # Close metrics div
                
                # Add research analysis section
                html_content += """
                    <h4>Research Analysis</h4>
                """
                
                if 'error' not in research:
                    html_content += f"""
                    <p><strong>Overall Sentiment:</strong> {research.get('sentiment', 'N/A')}</p>
                    """
                    
                    # Key drivers
                    if 'key_drivers' in research and research['key_drivers']:
                        html_content += "<h5>Key Drivers</h5><ul>\n"
                        if isinstance(research['key_drivers'], list):
                            for driver in research['key_drivers']:
                                html_content += f"<li>{driver}</li>\n"
                        else:
                            html_content += f"<li>{research['key_drivers']}</li>\n"
                        html_content += "</ul>\n"
                    
                    # Risks
                    if 'risks' in research and research['risks']:
                        html_content += "<h5>Potential Risks</h5><ul>\n"
                        if isinstance(research['risks'], list):
                            for risk in research['risks']:
                                html_content += f"<li>{risk}</li>\n"
                        else:
                            html_content += f"<li>{research['risks']}</li>\n"
                        html_content += "</ul>\n"
                    
                    # Future outlook
                    if 'future_outlook' in research:
                        html_content += f"<h5>Future Outlook</h5><p>{research['future_outlook']}</p>\n"
                    
                    # Recent news
                    if 'recent_news' in research and research['recent_news']:
                        html_content += """
                        <h5>Recent News</h5>
                        <table>
                            <tr>
                                <th>Date</th>
                                <th>Headline</th>
                                <th>Source</th>
                            </tr>
                        """
                        
                        for news_item in research['recent_news']:
                            html_content += f"""
                            <tr>
                                <td>{news_item['published']}</td>
                                <td><a href="{news_item['url']}" target="_blank">{news_item['headline']}</a></td>
                                <td>{news_item['source']}</td>
                            </tr>
                            """
                            
                        html_content += "</table>\n"
                else:
                    html_content += f"<p>Research analysis error: {research['error']}</p>\n"
                
                html_content += """
                </div>  <!-- Close position div -->
                """
            
            html_content += """
            </div>  <!-- Close account div -->
            """
        
        # Close HTML content
        html_content += """
        </body>
        </html>
        """
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write(html_content)
            
        self.logger.info(f"Generated report: {output_file}")
        return output_file