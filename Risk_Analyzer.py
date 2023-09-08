class RiskAnalyzer:
    def __init__(self, data):
        self.data = data
        
        # Weights for various components
        self.weights = {
            'issue_freq': 1,  # Weight for frequency of issue occurrence
            'manager_involvement': 5,  # Weight for manager involvement
            'parts_sent': 2,  # Weight for each part sent
            'repeat_parts_sent': 3,  # Weight for each repeated part sent
            'agent_tenure': -0.001,  # Negative weight for less experienced agents
            'warranty_priority': 4  # Weight for warranty ending soon
        }
    
    def _compute_issue_risk_score(self):
        # Aggregating necessary metrics by issue_type
        issue_aggregates = self.data.groupby('issue_type').agg({
            'repeat_ct': 'sum',
            'contact_manager_flg': 'sum',
            'parts_ct': 'sum',
            'repeat_parts_ct': 'sum',
            'agent_tenure_indays': 'mean',
            'contract_end': 'mean'
        }).reset_index()
        
        # Calculate a risk score based on various factors
        issue_aggregates['risk_score'] = (
            issue_aggregates['repeat_ct'] * self.weights['issue_freq'] +
            issue_aggregates['contact_manager_flg'] * self.weights['manager_involvement'] +
            issue_aggregates['parts_ct'] * self.weights['parts_sent'] +
            issue_aggregates['repeat_parts_ct'] * self.weights['repeat_parts_sent'] +
            issue_aggregates['agent_tenure_indays'] * self.weights['agent_tenure']
        )
        
        # Normalize contract_end dates to provide a priority score
        min_date = issue_aggregates['contract_end'].min()
        max_date = issue_aggregates['contract_end'].max()
        issue_aggregates['warranty_priority'] = (max_date - issue_aggregates['contract_end']).dt.days / (max_date - min_date).days
        
        # Combining the risk score and warranty priority
        issue_aggregates['final_score'] = issue_aggregates['risk_score'] + issue_aggregates['warranty_priority'] * self.weights['warranty_priority']
        
        return issue_aggregates[['issue_type', 'final_score']].sort_values('final_score', ascending=False)
    
    def rank_issues(self):
        return self._compute_issue_risk_score()


