import { Component } from '@angular/core';
import {ReadingService} from "../../services/reading.service";
import {Unit} from "../../models/unit";
import {Text} from "../../models/text";

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.scss']
})
export class TestComponent {

  unit: Unit | null = null
  text: Text | null = null

  constructor(private readingService: ReadingService) {

  }

  ngOnInit(): void {
    this.getTextDetail(1);
  }

  getTextDetail(titleId: number) {
    this.readingService.getText(titleId).subscribe({
      next: (result) => {
        this.text = result;
        for (const quest of this.text.quests) {
          console.log("quest: " + quest.quest)
          console.log("A: " + quest.option_a)
          console.log("B: " + quest.option_b)
          console.log("C: " + quest.option_c)
          console.log("D: " + quest.option_d)
        }
      }
    });
  }
}
