import {Quest} from "./quest";

export interface TextDetail {
  id: number;
  unit_name: string
  title: string
  context: string;
  quests: Quest[];
}
