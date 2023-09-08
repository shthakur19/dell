import unittest
import pandas as pd
from Risk_Analyzer import RiskAnalyzer

# Sample data
sample_data = {
    'issue_type': ['Issue A', 'Issue A', 'Issue B', 'Issue C'],
    'repeat_ct': [1, 1, 2, 0],
    'contact_manager_flg': [0, 1, 0, 0],
    'parts_ct': [2, 1, 3, 0],
    'repeat_parts_ct': [1, 1, 0, 0],
    'agent_tenure_indays': [300, 150, 500, 100],
    'contract_end': ['2023-05-01', '2023-05-15', '2023-06-01', '2023-04-01']
}
sample_df = pd.DataFrame(sample_data)
sample_df['contract_end'] = pd.to_datetime(sample_df['contract_end'])

class TestRiskAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = RiskAnalyzer(sample_df)
    
    def test_risk_score_calculation(self):
        result = self.analyzer._compute_issue_risk_score()
        #Assertions to compare the result's risk score with an expected value
        self.assertAlmostEqual(result.iloc[0]['final_score'], 20.34, places=1)  
    
    def test_rank_issues(self):
        result = self.analyzer.rank_issues()
        self.assertEqual(result.iloc[0]['issue_type'], 'Issue A')  
    

