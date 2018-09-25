import { Component, OnInit } from "@angular/core";
import { FormGroup, FormBuilder, FormArray, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router, ActivatedRoute } from "@angular/router";

import { AppConfig } from '@geonature_config/app.config';
import { CommonService } from '@geonature_common/service/common.service';


@Component({
  selector: "pnx-cmr-programs-form",
  templateUrl: "programs.form.component.html"
})
export class ProgramsFormComponent implements OnInit {
  
  public pgForm: FormGroup;
  public pg: any;
  public id_pg: number;

  constructor(
    private _pg: FormBuilder,
    private _api: HttpClient,
    private _route: ActivatedRoute,
    private _router: Router,
    private _commonService: CommonService
  ) { }

  postPg() {
    const pg = Object.assign({}, this.pgForm.value);
    let url = AppConfig.API_ENDPOINT + '/cmr/programs';
    if (this.id_pg) {
      url = url + '/' + this.id_pg;
    }
    this._api.post<any>( `${url}`, pg).subscribe(
      data => {
        this._router.navigate(['/cmr']);
        this._commonService.translateToaster('success', "Programe ajouté avec succès");
      },
      error => {
        this._commonService.translateToaster('error', 'ErrorMessage');
      }
    );
  }

  getPg(id_pg) {
    this._api.get<any>(`${AppConfig.API_ENDPOINT}/cmr/programs/${id_pg}`)
    .subscribe(data => {
      this.pg = data;
      this.pgForm.patchValue(data);
      console.log(data);
    })
  }

  ngOnInit() {
    this._route.params.subscribe(params => {
      this.id_pg = params['id'];
      if (this.id_pg) {
        this.getPg(this.id_pg);
      }
    });

    this.pgForm = this._pg.group({
      id_program:null,
      program_name: [null, Validators.required],
      program_desc: [null, Validators.required]
    });
  }
}

