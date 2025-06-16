import { AstrologyService } from './astrology.js';
import { NumerologyService } from './numerology.js';
import { FeedbackService } from './feedback.js';
import { CosmicFusionService } from './cosmic-fusion.js';

export class InsightsService {
  static async generateDailyInsight(
    sunSign: string,
    lifePathNumber: number,
    targetDate: string
  ): Promise<{
    overall_energy: number;
    love_energy: number;
    career_energy: number;
    health_energy: number;
    finance_energy: number;
    favorable_activities: string[];
    avoid_activities: string[];
    key_insights: string[];
  }> {
    const date = new Date(targetDate);
    const dayOfYear = Math.floor((date.getTime() - new Date(date.getFullYear(), 0, 0).getTime()) / 86400000);
    
    // Get AI learning insights for this user profile
    const learningInsights = await FeedbackService.getLearningInsights(sunSign, lifePathNumber);
    console.log('Learning insights:', learningInsights);
    
    // Create enhanced cosmic profile with fusion of astrology and numerology
    const cosmicProfile = CosmicFusionService.generateCosmicProfile(
      sunSign,
      lifePathNumber,
      lifePathNumber, // Using life path as destiny for simplification
      lifePathNumber, // Using life path as soul urge for simplification  
      lifePathNumber, // Using life path as personality for simplification
      new Date(targetDate).getDate() // Birth day from date
    );

    // Generate enhanced daily insights using cosmic fusion
    const enhancedInsights = CosmicFusionService.generateEnhancedDailyInsight(
      cosmicProfile,
      targetDate,
      learningInsights
    );

    // Convert enhanced insights to expected format
    const overall_energy = enhancedInsights.energyReadings.overall;
    const love_energy = enhancedInsights.energyReadings.love;
    const career_energy = enhancedInsights.energyReadings.career;
    const health_energy = enhancedInsights.energyReadings.health;
    const finance_energy = enhancedInsights.energyReadings.finance;

    // Combine cosmic influences with personalized guidance for key insights
    const key_insights = [
      ...enhancedInsights.cosmicInfluences.slice(0, 2),
      ...enhancedInsights.personalizedGuidance.slice(0, 2),
      `Manifestation power: ${enhancedInsights.manifestationPower}/10`,
      `Spiritual focus: ${enhancedInsights.spiritualFocus}`
    ];

    // Use enhanced activities but fall back to traditional if needed
    let favorable_activities = enhancedInsights.optimalActivities;
    let avoid_activities = enhancedInsights.cautionAreas;

    // Fallback to traditional method if enhanced doesn't provide enough
    if (favorable_activities.length === 0) {
      favorable_activities = this.getFavorableActivities(overall_energy, love_energy, career_energy);
    }
    
    if (avoid_activities.length === 0) {
      avoid_activities = this.getAvoidActivities(overall_energy, love_energy, career_energy);
    }

    return {
      overall_energy,
      love_energy,
      career_energy,
      health_energy,
      finance_energy,
      favorable_activities,
      avoid_activities,
      key_insights
    };
  }

  private static getFavorableActivities(overall: number, love: number, career: number): string[] {
    const activities: string[] = [];
    
    if (overall >= 7) activities.push('Starting new projects');
    if (love >= 7) activities.push('Romantic dates', 'Relationship conversations');
    if (career >= 7) activities.push('Job interviews', 'Business meetings', 'Networking');
    if (overall >= 6) activities.push('Creative pursuits');
    if (love >= 6) activities.push('Social gatherings');
    if (career >= 6) activities.push('Important decisions');
    
    return activities.length > 0 ? activities : ['Meditation', 'Self-reflection'];
  }

  private static getAvoidActivities(overall: number, love: number, career: number): string[] {
    const activities: string[] = [];
    
    if (overall <= 3) activities.push('Major life changes', 'Risky investments');
    if (love <= 3) activities.push('Difficult conversations', 'Confrontations');
    if (career <= 3) activities.push('Negotiations', 'Signing contracts');
    if (overall <= 4) activities.push('Travel', 'Public speaking');
    
    return activities.length > 0 ? activities : ['Avoid overthinking'];
  }

  static async generateActivityRecommendation(
    activityType: string,
    sunSign: string,
    lifePathNumber: number,
    daysAhead: number = 30
  ): Promise<{ date: string; confidence: number; reasoning: string }> {
    const today = new Date();
    
    // Get AI learning insights to improve confidence scoring
    const learningInsights = await FeedbackService.getLearningInsights(sunSign, lifePathNumber);
    
    // Create cosmic profile for enhanced recommendations
    const cosmicProfile = CosmicFusionService.generateCosmicProfile(
      sunSign,
      lifePathNumber,
      lifePathNumber,
      lifePathNumber,
      lifePathNumber,
      today.getDate()
    );
    
    // Enhanced algorithm to find optimal date using cosmic fusion
    let bestScore = 0;
    let bestDateStr = '';
    let bestReasoning = '';
    
    for (let i = 0; i < daysAhead; i++) {
      const checkDate = new Date(today);
      checkDate.setDate(today.getDate() + i);
      const dateStr = checkDate.toISOString().split('T')[0];
      
      // Generate enhanced insights for this date
      const enhancedInsights = CosmicFusionService.generateEnhancedDailyInsight(
        cosmicProfile,
        dateStr,
        learningInsights
      );
      
      let score = 0;
      let reasoning = '';
      
      // Enhanced scoring based on activity type and cosmic factors
      switch (activityType) {
        case 'wedding':
          score = enhancedInsights.energyReadings.love * 0.4 + 
                 enhancedInsights.energyReadings.overall * 0.3 +
                 enhancedInsights.manifestationPower * 0.3;
          reasoning = `Love energy (${enhancedInsights.energyReadings.love}/10) and manifestation power (${enhancedInsights.manifestationPower}/10) create ideal conditions for union and celebration`;
          break;
          
        case 'business_launch':
          score = enhancedInsights.energyReadings.career * 0.4 + 
                 enhancedInsights.energyReadings.finance * 0.3 + 
                 enhancedInsights.energyReadings.overall * 0.2 +
                 enhancedInsights.manifestationPower * 0.1;
          reasoning = `Career energy (${enhancedInsights.energyReadings.career}/10) and financial energy (${enhancedInsights.energyReadings.finance}/10) align for business success`;
          break;
          
        case 'travel':
          score = enhancedInsights.energyReadings.overall * 0.5 + 
                 enhancedInsights.energyReadings.health * 0.3 +
                 enhancedInsights.manifestationPower * 0.2;
          reasoning = `Overall energy (${enhancedInsights.energyReadings.overall}/10) and health energy (${enhancedInsights.energyReadings.health}/10) support safe and enjoyable travel`;
          break;
          
        case 'investment':
          score = enhancedInsights.energyReadings.finance * 0.5 + 
                 enhancedInsights.energyReadings.overall * 0.3 +
                 enhancedInsights.manifestationPower * 0.2;
          reasoning = `Financial energy (${enhancedInsights.energyReadings.finance}/10) and manifestation power create favorable conditions for investments`;
          break;
          
        case 'job_interview':
          score = enhancedInsights.energyReadings.career * 0.5 + 
                 enhancedInsights.energyReadings.overall * 0.3 +
                 enhancedInsights.manifestationPower * 0.2;
          reasoning = `Career energy (${enhancedInsights.energyReadings.career}/10) and personal magnetism favor professional success`;
          break;
          
        default:
          score = enhancedInsights.energyReadings.overall * 0.6 + 
                 enhancedInsights.manifestationPower * 0.4;
          reasoning = `Overall cosmic alignment and manifestation power create favorable conditions`;
      }
      
      // Boost score for optimal activities that match the activity type
      const optimalActivities = enhancedInsights.optimalActivities.join(' ').toLowerCase();
      if (optimalActivities.includes(activityType.replace('_', ' ')) || 
          optimalActivities.includes('important') || 
          optimalActivities.includes('business') ||
          optimalActivities.includes('meeting')) {
        score += 1;
        reasoning += '. Enhanced by cosmic activity alignment';
      }
      
      if (score > bestScore) {
        bestScore = score;
        bestDateStr = dateStr;
        bestReasoning = reasoning;
      }
    }
    
    // Enhanced confidence calculation
    let baseConfidence = Math.min(bestScore / 12, 0.95); // Adjusted for higher possible scores
    
    if (learningInsights && learningInsights.total_samples > 5) {
      const avgAccuracy = (learningInsights.accuracy_metrics.overall || 5) / 10;
      baseConfidence = (baseConfidence + avgAccuracy) / 2;
    }
    
    // Boost confidence based on cosmic alignment
    const alignmentBoost = (cosmicProfile.fusedInsights.cosmicAlignment - 5) * 0.05;
    baseConfidence = Math.min(0.95, Math.max(0.1, baseConfidence + alignmentBoost));
    
    const enhancedReasoning = `${bestReasoning}. Your ${sunSign} sun sign and life path ${lifePathNumber} combine with cosmic alignment (${cosmicProfile.fusedInsights.cosmicAlignment}/10) to create this optimal timing. ${learningInsights && learningInsights.total_samples > 5 ? `Confidence enhanced by ${learningInsights.total_samples} user feedback samples.` : ''}`;
    
    return {
      date: bestDateStr,
      confidence: baseConfidence,
      reasoning: enhancedReasoning
    };
  }
}
