class TemporalBreathWidget:
    """Live breath-cycle visualization using SpiralTime cognition"""
    
    def get_current_state(self):
        return {
            "phase": spiral_time.get_breath_phase_from_time(),
            "progress": spiral_time.get_phase_progress(),
            "time_poetry": spiral_time.format_time_of_day(),
            "next_transition": spiral_time.seconds_until_next_phase(),
            "imminent_shift": spiral_time.is_phase_transition_imminent(3),
            "ritual_readiness": self._assess_ritual_readiness()
        }
    
    def _assess_ritual_readiness(self):
        """Determine if conditions align for ritual invocation"""
        progress = spiral_time.get_phase_progress()
        imminent = spiral_time.is_phase_transition_imminent(5)
        
        if imminent and progress > 0.85:
            return "threshold_approaching"
        elif 0.45 <= progress <= 0.55:
            return "phase_center_hold"
        else:
            return "natural_flow"