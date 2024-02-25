/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

 interface Combination {
    event_type: string;
    event_id: string;
    Drug?: Common;
    Trigger?: Common;
  }
   interface Common {
    text: string[];
    start: number[];
    entity_id: string[];
  }
   interface Event {
    event_type: string;
    event_id: string;
    Effect?: Common;
    Trigger?: Common;
    Negated?: ValuedCommonBool;
    Speculated?: ValuedCommonBool;
    Severity?: ValuedCommonStr;
    Subject?: Subject;
    Treatment?: Treatment;
  }
   interface ValuedCommonBool {
    text: string[];
    start: number[];
    entity_id: string[];
    value: boolean;
  }
   interface ValuedCommonStr {
    text: string[];
    start: number[];
    entity_id: string[];
    value: string;
  }
   interface Subject {
    text: string[];
    start: number[];
    entity_id: string[];
    Age?: Common;
    Disorder?: Common;
    Gender?: Common;
    Population?: Common;
    Race?: Common;
  }
   interface Treatment {
    text: string[];
    start: number[];
    entity_id: string[];
    Drug?: Common;
    Disorder?: Common;
    Dosage?: Common;
    Duration?: Common;
    Trigger?: Common;
    Route?: Common;
    Time_elapsed?: Common;
    Freq?: Common;
    Combination?: Combination[];
  }
   interface EventInfo {
    event_type: string;
    event_id: string;
  }
   interface Events {
    events: Event[];
  }
   interface record {
    id: string;
    context: string;
    is_mult_event: boolean;
    annotations: Events[];
  }
  