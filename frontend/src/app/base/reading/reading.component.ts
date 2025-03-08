import { Component } from '@angular/core';
import {ReadingService} from "../../services/reading.service";
import {Unit} from "../../models/unit";
import {Text} from "../../models/text";


@Component({
  selector: 'app-reading',
  templateUrl: './reading.component.html',
  styleUrls: ['./reading.component.scss']
})
export class ReadingComponent {

  inputText: string = ''; // Kullanıcının girdiği metin
  outputText: string = ''; // Butona basıldığında gösterilecek metin

  text: Text | null = null

  units: Array<Unit> = []

  constructor(
    private readingService: ReadingService
  ) {}

  ngOnInit(): void {
    this.getUnits()
  }

  getUnits(){
    this.readingService.getUnits().subscribe({
      next: (result) => {
        this.units = result
      }
    });
  }

  updateText() {
    this.outputText = this.inputText; // Butona basıldığında input metnini output metnine aktar
  }
  getContainerHeight() {
    return this.outputText ? { 'reading-height': true } : { 'reading-full': true };
  }
  deleteText() {
    this.outputText = ""
    this.inputText = ""
  }

  getTextDetail(titleId: number) {
    this.readingService.getText(titleId).subscribe({
      next: (result) => {
        this.text = result
        for (const quest of this.text.quests) {
          console.log("quest: " + quest.quest)
          console.log("A: " + quest.option_a)
          console.log("B: " + quest.option_b)
          console.log("C: " + quest.option_c)
          console.log("D: " + quest.option_d)
        }
        this.inputText = this.text.context
      }
    });
  }
}
