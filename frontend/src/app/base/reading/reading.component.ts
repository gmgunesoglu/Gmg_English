import { Component } from '@angular/core';
import {ReadingService} from "../../services/reading.service";
import {Unit} from "../../models/unit";
import {TextDetail} from "../../models/text-detail";
import { Quest } from 'src/app/models/quest';
import { OptionType } from 'src/app/models/option-type';


interface AnsweredQuestiton {
  answered_option: OptionType,
  is_answer_correct: boolean,
}

@Component({
  selector: 'app-reading',
  templateUrl: './reading.component.html',
  styleUrls: ['./reading.component.scss']
})
export class ReadingComponent {

  inputText: string = '';
  outputText: string = '';

  isQuestsOpen: boolean = false;

  text_detail!: TextDetail;

  units: Array<Unit> = []
  option_types: OptionType[] = Object.values(OptionType);

  answeredQuestions: Map<number, AnsweredQuestiton> = new Map<number, AnsweredQuestiton>();

  constructor(
    private readingService: ReadingService
  ) {}

  ngOnInit(): void {
    this.getUnits();
  }

  getUnits(){
    this.readingService.getUnits().subscribe({
      next: (result) => {
        this.units = result
      }
    });
  }

  updateText() {
    this.outputText = this.inputText;
  }


  deleteText() {
    this.outputText = ""
    this.inputText = ""
  }

  getTextDetail(titleId: number) {
    this.readingService.getTextDetail(titleId).subscribe({
      next: (result) => {
        this.text_detail = result
        this.inputText = this.text_detail.context
      }
    });
  }

  checkReading() {

  }

  openQuests() {
    if (this.text_detail !== null && this.text_detail.quests.length > 0){
      this.isQuestsOpen = true;
    }
  }

  closeQuests() {
    this.isQuestsOpen = false;
  }

  optionSelected(quest: Quest, option: OptionType): void {

    if (this.answeredQuestions.has(quest.id)) {
      return;
    }

    this.answeredQuestions.set(quest.id, {
      answered_option: option,
      is_answer_correct: option === quest.correct_option,
    })

    console.log(`Seçilen soru: ${quest.quest}`);
    console.log(`Seçilen seçenek: ${option}`);
    console.log(`correct_answer: ${quest.correct_option}`);
    console.log(`answer is correct?: ${option === quest.correct_option}`);
  }

  getOptionClass(quest: Quest, option: OptionType): string {
  if (!this.answeredQuestions.has(quest.id) || this.answeredQuestions.get(quest.id)?.answered_option !== option) {
    return '';
  }
  return this.answeredQuestions.get(quest.id)?.is_answer_correct ? "answer-correct" : "answer-wrong"
  }

  isAnswered(quest: Quest): boolean {
    return this.answeredQuestions.has(quest.id);
  }
}
