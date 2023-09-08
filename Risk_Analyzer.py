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
    
    def compute_individual_risk_score(self):
        #Computing general risk score for each issue_type
        issue_aggregates = self.data.groupby('issue_type').agg({
        'repeat_ct': 'sum',
        'contact_manager_flg': 'sum',
        'parts_ct': 'sum',
        'repeat_parts_ct': 'sum',
        'agent_tenure_indays': 'mean'
         }).reset_index()
    
        issue_aggregates['risk_score'] = (
        issue_aggregates['repeat_ct'] * self.weights['issue_freq'] +
        issue_aggregates['contact_manager_flg'] * self.weights['manager_involvement'] +
        issue_aggregates['parts_ct'] * self.weights['parts_sent'] +
        issue_aggregates['repeat_parts_ct'] * self.weights['repeat_parts_sent'] +
        issue_aggregates['agent_tenure_indays'] * self.weights['agent_tenure'])
    
        # Merging this general risk score with the main dataframe on issue_type
        merged_data = self.data.merge(issue_aggregates[['issue_type', 'risk_score']], on='issue_type', how='left')
    
        # Computing warranty priority score for each request and combining  with the general risk score
        min_date = merged_data['contract_end'].min()
        max_date = merged_data['contract_end'].max()
        merged_data['warranty_priority'] = (max_date - merged_data['contract_end']).dt.days / (max_date - min_date).days
        merged_data['final_score'] = merged_data['risk_score'] + merged_data['warranty_priority'] * self.weights['warranty_priority']
        
        #Sorting the dataframe based on the combined risk score
        prioritized_data = merged_data.sort_values('final_score', ascending=False)
        
        return prioritized_data

    
    
    def rank_issues(self):
        return self.compute_individual_risk_score()


