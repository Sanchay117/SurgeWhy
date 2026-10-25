export type SceneId = "open" | "zetaris" | "counterfactual" | "engines" | "outro";

export const NARRATION_VOICE = "aura-2-thalia-en";

export interface NarrationScene {
  id: SceneId;
  lead: number;
  tail: number;
  lines: { text: string; say?: string }[];
}

export const NARRATION: NarrationScene[] = [
  {
    id: "open",
    lead: 0.45,
    tail: 0.7,
    lines: [
      {
        text: "Your flight to London lands four and a half hours late, and twelve seconds after you file a claim, the airline bot replies: Denied, zero dollars, extraordinary weather.",
      },
      {
        text: "Over $6.8 billion in valid passenger compensation goes unpaid every year because travelers cannot see inside the black box.",
        say: "Over six point eight billion dollars in valid passenger compensation goes unpaid every year, because travelers cannot see inside the black box.",
      },
      {
        text: "Meet SurgeWhy: an explainable multi-agent adjudicator that proves why your flight was actually delayed, rules out false excuses, and shows what flips the verdict.",
      },
    ],
  },
  {
    id: "zetaris",
    lead: 0.4,
    tail: 0.65,
    lines: [
      {
        text: "In Layer 01 Data, SurgeWhy queries four independent aviation and legal sources through Zetaris using single-statement REST SQL.",
        say: "In Layer zero one Data, SurgeWhy queries four independent aviation and legal sources through Zetaris, using single statement REST sequel.",
      },
      {
        text: "On flight UA-418 from San Francisco to Heathrow, NOAA METAR weather shows ten-mile clear skies and all fourteen neighboring flights departing on time.",
        say: "On flight U A four eighteen from San Francisco to Heathrow, Noah metar weather shows ten mile clear skies, and all fourteen neighboring flights departing on time.",
      },
      {
        text: "Tail logs on N784UA expose the real cause: a 148-minute brake sensor repair that pushed the first officer past FAA duty limits, unlocking $890 under UK261.",
        say: "Tail logs on N seven eighty four U A expose the real cause: a one hundred forty eight minute brake sensor repair that pushed the first officer past F A A duty limits, unlocking eight hundred ninety dollars under U K two sixty one.",
      },
    ],
  },
  {
    id: "counterfactual",
    lead: 0.4,
    tail: 0.65,
    lines: [
      {
        text: "Built for Track 2, SurgeWhy explains not only why you won, but the exact counterfactual boundary that flips the decision.",
        say: "Built for Track two, SurgeWhy explains not only why you won, but the exact counterfactual boundary that flips the decision.",
      },
      {
        text: "Slide arrival delay twenty-six minutes earlier and statutory cash drops fifty percent; activate an FAA Ground Stop and delay cash flips to zero while hotel care stays mandatory.",
        say: "Slide arrival delay twenty six minutes earlier and statutory cash drops fifty percent. Activate an F A A Ground Stop and delay cash flips to zero, while hotel care stays mandatory.",
      },
      {
        text: "And when Lufthansa 455 has a seven-minute cabin door sensor gap right across the three-hour legal cliff, SurgeWhy pauses at 62% confidence and requests one arrival photo instead of guessing.",
        say: "And when Lufthansa four fifty five has a seven minute cabin door sensor gap right across the three hour legal cliff, SurgeWhy pauses at sixty two percent confidence, and requests one arrival photo instead of guessing.",
      },
    ],
  },
  {
    id: "engines",
    lead: 0.4,
    tail: 0.65,
    lines: [
      {
        text: "In Layer 02 Build, crafted with Cursor and all four Meterless Engines, SurgeWhy uses an adversarial Airline Defense Counsel Critic.",
        say: "In Layer zero two Build, crafted with Cursor and all four Meterless Engines, SurgeWhy uses an adversarial Airline Defense Counsel Critic.",
      },
      {
        text: "Scout Intent routes the dispute, H-MEM recalls carrier pretext patterns, and the Counsel Critic blocks Round 1 until tail logs rule out inbound bird strikes inside the versioned World Model.",
        say: "Scout Intent routes the dispute, H mem recalls carrier pretext patterns, and the Counsel Critic blocks Round one until tail logs rule out inbound bird strikes inside the versioned World Model.",
      },
      {
        text: "Meanwhile, the Markovian engine compresses multi-step forensic history into compact proof capsules, cutting cumulative prompt tokens by over 91%.",
        say: "Meanwhile, the Markovian engine compresses multi step forensic history into compact proof capsules, cutting cumulative prompt tokens by over ninety one percent.",
      },
    ],
  },
  {
    id: "outro",
    lead: 0.4,
    tail: 0.85,
    lines: [
      {
        text: "In Layer 03 Power, Meterless Nightshift routes fast SQL discovery to NVIDIA Nemotron 30B Lightning, and deep legal critique and counterfactual math to Nemotron 120B Super.",
        say: "In Layer zero three Power, Meterless Nightshift routes fast sequel discovery to Nvidia Nemotron thirty B Lightning, and deep legal critique and counterfactual math to Nemotron one twenty B Super.",
      },
      {
        text: "Every step logs a verifiable Nightshift model receipt alongside a ready-to-send passenger legal demand notice.",
      },
      {
        text: "Three of three smoke checks and nine conformance tests pass in milliseconds. SurgeWhy: auditable proof when the black box says no.",
      },
    ],
  },
];
