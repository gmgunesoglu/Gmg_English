import { OptionType } from "./option-type";

export interface CreateQuest {
  text_id: number;
  quest: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  correct_option: OptionType;
  justification: string;
}
