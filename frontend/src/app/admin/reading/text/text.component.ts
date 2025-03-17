import {Component, Input, Output, EventEmitter, ViewChild} from '@angular/core';
import {TextDetail} from "../../../models/text-detail";
import {UpdateText} from "../../../models/update-text";
import { ReadingService } from "../../../services/reading.service";
import { CreateQuest } from 'src/app/models/create-quest';
import { OptionType } from 'src/app/models/option-type';
import { Quest } from 'src/app/models/quest';
import { UpdateQuest } from 'src/app/models/update-quest';

@Component({
  selector: 'app-text',
  templateUrl: './text.component.html',
  styleUrls: ['./text.component.scss']
})
export class TextComponent {
  @Input() text_detail!: TextDetail;
  @Input() unit_id!: number;
  @Output() back = new EventEmitter<void>();

  is_updating_text: boolean = false;
  is_creating_quest: boolean = false;
  is_updating_quest: boolean = false;
  update_text!: UpdateText;
  titlePattern = '^(?!\\s*$).+';
  create_quest!: CreateQuest;
  option_types = Object.values(OptionType);
  selected_quest!: Quest;
  update_quest!: UpdateQuest;

  constructor(
    private readingService: ReadingService,

  ) {
  }

  ngOnInit(): void {
    this.update_text = {
      unit_id: this.unit_id,
      context: "",
      title: "",
    }
    this.resetNewQuest();
  }

  closeText(): void {
    this.back.emit();
  }

  updateText() {
    this.update_text.title = this.text_detail.title;
    this.update_text.context = this.text_detail.context;
    this.is_updating_text = true;
  }

  cancelUpdateText() {
    this.is_updating_text = false;
  }

  saveUpdateText() {
    this.readingService.updateText(this.update_text, this.text_detail.id).subscribe(
      (result) => {
        console.log(result);
        this.refrestTextDetail();
      },
      (error) => {
        alert(error.error);
        console.log(error);
      }
    );
    this.is_updating_text = false;
  }

  createQuest(): void {
    this.is_creating_quest = true;
  }

  cancelCreateText(): void {
    this.is_creating_quest = false;
    this.resetNewQuest();
  }

  saveQuest(): void {
    this.readingService.createQuest(this.create_quest).subscribe(
      (result) => {
        console.log(result);
        this.refrestTextDetail();
        this.resetNewQuest();
      },
      (error) => {
        alert(error.error);
        console.log(error);
      }
    );

  }

  deleteQuest(quest_id: number): void {
    this.readingService.deleteQuest(quest_id).subscribe(
      (result) => {
        console.log(result);
        this.refrestTextDetail();
      },
      (error) => {
        alert(error.error);
        console.log(error);
      }
    );
    this.resetNewQuest();
  }

  cancelUpdateQuest(): void {
    this.is_updating_quest = false;
  }

  openUpdateQuestForm(quest: Quest): void{
    this.selected_quest = quest;
    this.is_updating_quest = true;
    const { id, ...rest } = quest
    this.update_quest = rest
  }

  updateQuest(): void {
    this.readingService.updateQuest(this.update_quest, this.selected_quest.id).subscribe(
      (result) => {
        console.log(result);
        this.refrestTextDetail();
        this.is_updating_quest = false;
      },
      (error) => {
        alert(error.error);
        console.log(error);

      }
    );
  }

  resetNewQuest(): void {
    this.create_quest = {
      text_id: this.text_detail.id,
      quest: "",
      option_a: "",
      option_b: "",
      option_c: "",
      option_d: "",
      correct_option: OptionType.A,
      justification: "",
    }
  }

  refrestTextDetail(): void {
    this.readingService.getTextDetail(this.text_detail.id).subscribe(
      (result) => {
        this.text_detail = result;
      }
    );
  }
}
