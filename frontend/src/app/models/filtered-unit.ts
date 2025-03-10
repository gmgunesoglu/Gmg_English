import {Title} from "./title";

export interface FilteredUnit {
  id: number;
  name: string;
  titles: Title[];
  show_titles: boolean;
}
