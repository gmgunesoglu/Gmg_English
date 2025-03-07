import { Title } from "./title";

export interface Unit {
  id: number;
  name: string;
  titles: Title[];
  showTitles?: boolean;
}
