import { Component, OnInit } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { AppConfig } from '@geonature_config/app.config';
import { Router } from "@angular/router";


@Component({
  selector: "pnx-cmr-programs",
  templateUrl: "programs.list.component.html"
})
export class ProgramsListComponent implements OnInit {
  public programs: Array<any>;
  constructor(
    private _api: HttpClient,
    private _router: Router
  ) { }

  onAddProgram() {
    this._router.navigate(["cmr/form_pg"]);
  }

  pgEdit(id_pg) {
    this._router.navigate(['cmr/form_pg', id_pg]);
  }

  ngOnInit() {
    this._api.get<any>(`${AppConfig.API_ENDPOINT}/cmr/programs`)
      .subscribe(data => {
        this.programs = data;
        console.log(data);
      })

  }
}
